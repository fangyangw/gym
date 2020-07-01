from Fitness import models
import datetime
import pytz
import math
from Fit.settings import FREE_DAY, FREE_CARD_NAME, DISCOUNT_PRICE, DICCOUNT_REMARK, NOTICE_NAME, NOTICE_REMARK
from django.db.models import Q
from Fitness.utils.wechatConfig import defaults
from Fitness.utils.common_tools import call_api
from Fitness.utils.wechatConfig import notice_template_id, notice_url


def check_and_activation_card(member, user_card):
    user_door_log = models.DoorControlLog.objects.filter(userID=str(member.MID)).first()
    remain_days = get_user_remain_time(member)[0]
    if user_door_log and remain_days < 1:
        activation_card(user_card)


def activation_card(user_card):
    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
    expiration = utc_now
    if user_card.CARD_ID:
        expiration = utc_now + datetime.timedelta(days=int(user_card.CARD_ID.DAYS))
    elif user_card.REMARK == FREE_CARD_NAME:
        expiration = utc_now + datetime.timedelta(days=FREE_DAY)
    if user_card.ACTIVATION_DATE is None:
        user_card.ACTIVATION_DATE = utc_now
        user_card.EXPIRATION_TIME = expiration
        user_card.save()


def get_user_remain_time(member):
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
    remain_time = 0
    try:
        cards = models.UserCard.objects.filter(MEMBER_ID=member).order_by('id')
        inuse_card = None
        total_days = 0
        for card in cards:
            if card.REMARK == FREE_CARD_NAME and card.ACTIVATION_DATE is None:
                if not inuse_card:
                    inuse_card = card
                total_days += FREE_DAY
            elif card.ACTIVATION_DATE:
                if card.EXPIRATION_TIME and card.EXPIRATION_TIME > now:
                    if not inuse_card:
                        inuse_card = card
                    total_days += math.ceil((card.EXPIRATION_TIME - now).total_seconds() / (24 * 60 * 60))
            else:
                if not inuse_card:
                    inuse_card = card
                total_days += int(card.CARD_ID.DAYS)
        return total_days, inuse_card
    except Exception as e:
        print("get remain time error, %s" % str(e))
    return remain_time, None


def get_user_discount(member):
    price = DISCOUNT_PRICE[0]
    discount_card = models.Card.objects.filter(REMARK=DICCOUNT_REMARK).first()
    if member:
        try:
            now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('Asia/Shanghai'))
            cards = models.UserCard.objects.filter(MEMBER_ID=member, CARD_ID=discount_card).filter(~Q(REMARK=FREE_CARD_NAME)).order_by('id')
            status = []
            for i, count in enumerate(DISCOUNT_PRICE[1:]):
                status.append({
                    "price": count,
                    "stat": False,
                    "index": i + 1
                })
            for card in cards:
                if card.create_time:
                    create_time = card.create_time.replace(tzinfo=pytz.timezone("UTC")).astimezone(pytz.timezone('Asia/Shanghai'))
                    for item in status:
                        if create_time.month == now.month - item["index"]:
                            item["stat"] = True

            for item in status:
                if item["stat"] is False:
                    return price
                price = item["price"]

        except Exception as e:
            print("get remain time error, %s" % str(e))
    return price


def send_notification(member, card):
    if card and card.EXPIRATION_TIME:
        payload = """
    {
        "touser":"%s",
        "template_id":"%s",
        "url":"%s",
        "topcolor":"#FF0000",
        "data":{
            "name":{
                "value":"%s"
            },
            "expDate":{
                "value":"%s"
            },
            "remark":{
                "value": "%s"
            }
        }
    } 
    """ % (member.OPENID, notice_template_id, notice_url, NOTICE_NAME, card.EXPIRATION_TIME.strftime("%Y年%m月%d日"), NOTICE_REMARK)
        token = models.Config.objects.filter(key="access_token").first()
        notice_user_url = "%s?access_token=%s" % (defaults.get("notice_user_url"), token.value)
        response = call_api("POST", notice_user_url, payload, "notice_user")
        if response and response.get("errcode") == 0:
            print("notice status: ok.")
            member.notice_status = True
            member.save()
        else:
            print("notice status: error.")
