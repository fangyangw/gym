from django.conf import settings
from django.views import View
from django.utils import timezone
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import permissions
import pytz

from Fitness.utils.serializer import OrderSerialzier, QuerySerializer
from Fitness.models import Order, Member, Card, Course, UserProfile, Config, UserCard, UserCourse

from Fitness.utils.common_tools import nonce_str as generate_nonce_str
from Fitness.utils.common_tools import sign as sign_func
from Fitness.utils.common_tools import sign_sha1
from Fitness.utils.core import IsOpenIDAuthentication

from Fitness.utils.wechatConfig import APPID, MCH_ID, NOTIFY_URL, SIGN_KEY, UNIFIED_ORDER_URL, ORDER_QUERY_URL
from rest_framework.decorators import api_view
from Fitness.views.tools import check_and_activation_card

import time
import hashlib
import json
import dicttoxml
import xmltodict
import requests
import datetime
from Fitness.views.yibi import check_and_finish_order_rewards


class OrderView(GenericAPIView):
    serializer_class = OrderSerialzier
    # require open_id have in UserProfile
    permission_classes = (IsOpenIDAuthentication, ) #(permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        busname = serializer.validated_data.get("busname")
        description = serializer.validated_data.get("description")
        total_fee = serializer.validated_data.get("total_fee")
        open_id = serializer.validated_data.get("open_id")
        good_id = serializer.validated_data.get("good_id")

        appid = APPID
        mch_id = MCH_ID

        nonce_str = generate_nonce_str()
        trade_type = "JSAPI" #"APP"
        notify_url = NOTIFY_URL

        if "HTTP_X_FORWARDED_FOR" in request.META:
            spbill_create_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            spbill_create_ip = request.META['REMOTE_ADDR']

        instance = Order.objects.create(
            busname=busname,
            description=description,
            total_fee=total_fee,
            open_id=open_id,
            good_id=good_id
        )

        instance.out_trade_no = timezone.now().strftime("%Y%m%d") + '{}'.format(instance.id)
        instance.save()

        payload = {
            "appid": appid,
            "mch_id": mch_id,
            "nonce_str": nonce_str,
            "body": "易在24h健身-会员充值",
            "out_trade_no": instance.out_trade_no,
            "total_fee": total_fee,
            "spbill_create_ip": spbill_create_ip,
            "notify_url": notify_url,
            "trade_type": trade_type,
            "scene_info": '{"h5_info": {"type":"Wap","wap_url": "https:///www.ezaifit.top","wap_name": "会员充值"}}',
            "openid": open_id
        }

        sign = sign_func(payload, SIGN_KEY)
        payload["sign"] = sign

        req_xml = dicttoxml.dicttoxml(payload, custom_root="xml")
        url = UNIFIED_ORDER_URL

        res_xml = requests.post(url, req_xml, verify=False)
        res_xml.encoding = 'utf8'
        res_xml = res_xml.text
        res_obj = xmltodict.parse(res_xml)["xml"]
        return_code = res_obj["return_code"]

        if return_code == "FAIL":
            res = {
                "code": -1,
                "message": res_obj["return_msg"]
            }
        else:
            result_code = res_obj["result_code"]
            if result_code == "SUCCESS":
                prepay_id = res_obj["prepay_id"]
                instance.prepay_id = prepay_id
                instance.save()
                ts = int(time.time())
                # nonce_str = generate_nonce_str()
                package = 'Sign=WXPay'
                sign_type = "MD5"

                sign_payload = {
                    'appId': appid,
                    'signType': sign_type,
                    'nonceStr': nonce_str,
                    'timeStamp': ts,
                    'package': "prepay_id=" + prepay_id
                }

                pay_sign = sign_func(sign_payload, SIGN_KEY)

                res = {
                    "code": 0,
                    "message": "ok",
                    "timestamp": ts,
                    "nonce_str": nonce_str,
                    "package": package,
                    "sign_type": sign_type,
                    "pay_sign": pay_sign,
                    "prepay_id": prepay_id,
                    "out_trade_no": instance.out_trade_no,
                    "partner_id": mch_id
                }
            else:
                res = {
                    "code": 1,
                    "message": res_obj["err_code_des"]
                }

        return Response(res)

# 微信通知
class PayNotifyView(View):

    def post(self, request, *args, **kwargs):
        raw_data = request.read()
        print('---', raw_data)
        xml_obj = xmltodict.parse(raw_data)["xml"]
        print('-=', xml_obj)
        return_code = xml_obj["return_code"]
        if return_code != "SUCCESS":
            pass
        else:
            result_code = xml_obj["result_code"]
            if result_code == "SUCCESS":
                bank_type = xml_obj["bank_type"]
                total_fee = xml_obj["total_fee"]
                cash_fee = xml_obj.get("cash_fee")
                transaction_id = xml_obj["transaction_id"]
                out_trade_no = xml_obj["out_trade_no"]
                time_end = timezone.datetime.strptime(xml_obj["time_end"], "%Y%m%d%H%M%S")
                order = Order.objects.filter(out_trade_no=out_trade_no).first()
                if order:
                    member = Member.objects.filter(OPENID=order.open_id).first()
                    if member:
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
                        member.save()
                    if "%s" % order.total_fee == "%s" % total_fee:
                        order.bank_type = bank_type
                        order.cash_fee = cash_fee
                        order.transaction_id = transaction_id
                        order.time_end = time_end
                        order.status = True
                        order.save()
                        check_and_finish_order_rewards(member, member.SHARE, order)

        res_xml = """<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"""
        return HttpResponse(res_xml, content_type="application/xml")


class OrderQueryView(GenericAPIView):
    serializer_class = QuerySerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prepay_id = serializer.validated_data.get("prepay_id")
        out_trade_no = serializer.validated_data.get("out_trade_no")

        instance = Order.objects.filter(out_trade_no=out_trade_no).first()
        if not instance:
            return Response({"code": -1, "message": "订单号错误"})
        if instance.status == "1":
            return Response({"code": 0, "message": "支付成功"})
        appid = APPID
        mch_id = MCH_ID
        nonce_str = generate_nonce_str()
        payload = {
            "appid": appid,
            "mch_id": mch_id,
            "nonce_str": nonce_str,
            "out_trade_no": out_trade_no
        }
        sign = sign_func(payload, SIGN_KEY)
        payload["sign"] = sign
        req_xml = dicttoxml.dicttoxml(payload, custom_root="xml")
        url = ORDER_QUERY_URL
        res_xml = requests.post(url, req_xml, verify=False)
        res_xml.encoding = 'utf8'
        res_xml = req_xml.text
        res_obj = xmltodict.parse(res_xml)["xml"]
        return_code = res_obj["return_code"]
        if return_code == "FAIL":
            res = {
                "code": -1,
                "message": res_obj["return_msg"]
            }
        else:
            result_code = res_obj["result_code"]
            trade_state = res_obj["trade_state"]
            if result_code == "SUCCESS" and trade_state == "SUCCESS":
                appid = res_obj["appid"]
                mch_id = res_obj["mch_id"]
                nonce_str = res_obj["nonce_str"]
                sign = res_obj["sign"]
                openid = res_obj["openid"]
                trade_type = res_obj["trade_type"]
                bank_type = res_obj["bank_type"]
                total_fee = res_obj["total_fee"]
                cash_fee = res_obj.get("cash_fee")
                transaction_id = res_obj["transaction_id"]
                out_trade_no = res_obj["out_trade_no"]
                time_end = timezone.datetime.strptime(
                    res_obj["time_end"], "%Y%m%d%H%M%S")
                order = Order.objects.filter(
                    openid=openid, out_trade_no=out_trade_no)
                if order:
                    if order.total_fee == total_fee:
                        order.bank_type = bank_type
                        order.cash_fee = cash_fee
                        order.transaction_id = transaction_id
                        order.time_end = time_end
                        order.status = True
                        order.save()
                        return Response({"code": 0, "message": "支付成功"})
        return Response({"code": 1, "message": "支付未完成"})


@api_view(['POST'])
def get_app_sign(request):
    open_id = request.data.get("open_id")
    location = request.data.get("location")
    open_location = request.data.get("open_location")
    print("upload photo log ", open_id, location)
    user = UserProfile.objects.filter(openid=open_id).first()
    if not user:
        return Response({
            "code": -1,
            "message": "用户未授权open id"
        })
    ts = int(time.time())
    nonce_str = generate_nonce_str()
    # package = 'Sign=WXPay'
    # sign_type = "MD5"
    jsapi_ticket = Config.objects.filter(key="jsapi_ticket").first()

    url = "https://www.ezaifit.top/User/UploadPhoto"
    if open_location:
        url = "https://www.ezaifit.top/User"
    sign_payload = {
        # 'appId': APPID,
        # 'signType': sign_type,
        # 'nonceStr': nonce_str,
        # 'timeStamp': ts,
        # 'package': "prepay_id=" + prepay_id
        "noncestr": nonce_str,
        "jsapi_ticket": jsapi_ticket.value,
        "timestamp": ts,
        "url": url
    }
    pay_sign = sign_sha1(sign_payload)

    res = {
        "code": 0,
        "message": "ok",
        "timestamp": ts,
        "nonce_str": nonce_str,
        # "package": package,
        # "sign_type": sign_type,
        "pay_sign": pay_sign,
        # "prepay_id": prepay_id,
        # "out_trade_no": instance.out_trade_no,
        # "partner_id": mch_id
    }
    return Response(res)
