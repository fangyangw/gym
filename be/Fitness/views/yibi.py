# 会员易币
from rest_framework.views import APIView
from rest_framework.response import Response
from Fitness.models import YibiOrder, UserProfile, Member, UserCard, Card, Course, UserCourse
from Fit.settings import YIBI_NUMBER_FROM_SHARE, IS_ON_SALE, FREE_DAY, FREE_CARD_NAME, FIRST_ORDER_REWARD_RATE
from Fitness.utils import serializer
from Fitness.views.tools import check_and_activation_card
from django.db import transaction
import datetime
from rest_framework.decorators import api_view
from django.db.models import Q
import pytz

SHARE_TYPE = "rewards_from_share"
BUY_GOOD = "buy_good"
SYSTEM_PAYER = "SYSTEM"
FIRST_REWARD_TYPE = "first_order_rewards_from_share"


@transaction.atomic
def check_and_finish_order_rewards(member, recommend_id, the_order):
    if not recommend_id:
        return
    user = UserProfile.objects.filter(openid=member.OPENID).first()
    order = YibiOrder.objects.filter(trade_type=FIRST_REWARD_TYPE, other_id=member.OPENID, payee=recommend_id).first()
    order_reverse = YibiOrder.objects.filter(trade_type=FIRST_REWARD_TYPE, other_id=recommend_id, payee=member.OPENID).first()
    if not order and not order_reverse:
        if the_order and the_order.status is True:
            total_yibi = (the_order.total_fee / 100) * FIRST_ORDER_REWARD_RATE
            share_order = YibiOrder(trade_type=FIRST_REWARD_TYPE, other_id=member.OPENID,
                                    payee=recommend_id, total_yibi=total_yibi,
                                    payer=SYSTEM_PAYER, status=True, description="first order rewards from recommand")
            recommend_member = Member.objects.filter(OPENID=recommend_id).first()
            if recommend_member:
                share_order.save()
                recommend_member.YIBI = str(int(recommend_member.YIBI) + YIBI_NUMBER_FROM_SHARE)
                recommend_member.save()


@transaction.atomic
def check_and_finish_recommend(member, recommend_id):
    user = UserProfile.objects.filter(openid=member.OPENID).first()
    order = YibiOrder.objects.filter(trade_type=SHARE_TYPE, other_id=member.OPENID, payee=recommend_id).first()
    order_reverse = YibiOrder.objects.filter(trade_type=SHARE_TYPE, other_id=recommend_id, payee=member.OPENID).first()
    if not order and not order_reverse:
        if member.PHONE and member.PHONE != '0' and member.PICTURE and member.PICTURE != '' and user.subscribe == 1:
            share_order = YibiOrder(trade_type=SHARE_TYPE, other_id=member.OPENID,
                                    payee=recommend_id, total_yibi=YIBI_NUMBER_FROM_SHARE,
                                    payer=SYSTEM_PAYER, status=True, description="share have finish, got 10 yibi")
            recommend_member = Member.objects.filter(OPENID=recommend_id).first()
            if recommend_member:
                share_order.save()
                recommend_member.YIBI = str(int(recommend_member.YIBI) + YIBI_NUMBER_FROM_SHARE)
                recommend_member.save()


def check_and_set_free_data(member):
    user = UserProfile.objects.filter(openid=member.OPENID).first()
    free_card = UserCard.objects.filter(MEMBER_ID=member, REMARK=FREE_CARD_NAME).first()
    if not free_card and member.PHONE and member.PHONE != '0' and member.PICTURE and member.PICTURE != '' and user.subscribe == 1:
        ## 新会员注册
        if IS_ON_SALE:
            free_card = UserCard(
                MEMBER_ID=member,
                REMARK=FREE_CARD_NAME,
            )
            free_card.save()


@api_view(['GET'])
def get_yibi_order(request):
    open_id = request.GET.get("open_id")
    member = Member.objects.filter(OPENID=open_id).first()
    res = {
        'code': 200,
        'data': [],
        'msg': 'Success'
    }
    if member:
        condition = Q(payee=member.OPENID) | Q(payer=member.OPENID)
        yibi_set = YibiOrder.objects.filter(condition).filter(status=True)
        yibi_data = serializer.YibiOrderSerializer(data=yibi_set, many=True)
        yibi_data.is_valid()
        res['data'] = yibi_data.data
    return Response(res)


@api_view(['POST'])
@transaction.atomic
def buy_use_yibi(request):
    open_id = request.data.get("open_id")
    total_yibi = int(request.data.get("total_yibi"))
    busname = request.data.get("busname")
    good_id = request.data.get("good_id")
    description = request.data.get("description")
    member = Member.objects.filter(OPENID=open_id).first()
    res = {
        'code': 200,
        'data': [],
        'message': 'Success'
    }
    if member:
        if member.YIBI and int(member.YIBI) >= total_yibi:
            order = YibiOrder(trade_type=BUY_GOOD, other_id=member.OPENID,
                                    payee=SYSTEM_PAYER, total_yibi=total_yibi,
                                    payer=member.OPENID, status=True, description=description,
                                    good_id=good_id, busname=busname)
            member.YIBI = str(int(member.YIBI) - total_yibi)
            member.save()
            order.save()
            if order.busname == 'card':
                card = Card.objects.filter(CID=order.good_id).first()
                if card:
                    member.CARD_ID = card
                    user_card = UserCard(MEMBER_ID=member, CARD_ID=card)
                    check_and_activation_card(member, user_card)
                    user_card.save()

            elif order.busname == 'class':
                course = Course.objects.filter(CID=order.good_id).first()
                if course:
                    member.COURSE_ID = course
                    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC'))
                    expiration = utc_now + datetime.timedelta(days=course.DAYS)
                    user_course = UserCourse(MEMBER_ID=member, COURSE_ID=course,
                                    ACTIVATION_DATE=utc_now, EXPIRATION_TIME=expiration)
                    user_course.save()
            res['message'] = "购买成功"
        else:
            res['code'] = 500
            res['message'] = "易币余额不足"
    else:
        res['code'] = 500
        res['message'] = "用户未授权"
    return Response(res)

class YiBi(APIView):
    pass
