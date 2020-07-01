# 会员手机号
from rest_framework.views import APIView
from rest_framework.response import Response
from Fitness import models
from Fitness.utils import serializer
from rest_framework.decorators import api_view
import datetime
from Fit.settings import verification_code_in_date, sms_send_uri, sms_account, sms_password, sms_template
import random
import json
import urllib
import requests
import pytz
from Fitness.views.member import check_and_set_recommend


@api_view(['POST'])
def send_verification_code(request):
    res = {
        "code": 0,
        "message": ""
    }
    open_id = request.data.get("open_id")
    phone_number = request.data.get("phone_number")
    member = models.Member.objects.filter(OPENID=open_id).first()
    if not member:
        return Response({
            "code": -1,
            "message": "用户未授权open id"
        })
    in_date = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) + datetime.timedelta(minutes=verification_code_in_date)
    verification_code = random.randint(100000, 999999)
    text = sms_template % verification_code
    params = {'account': sms_account,
              'password': sms_password,
              'msg': urllib.request.quote(text),
              'phone': phone_number,
              'report': 'false'
        }
    params = json.dumps(params)

    headers = {"Content-type": "application/json"}
    response = requests.request("POST", sms_send_uri, data=params, headers=headers)
    if response.status_code == 200:
        r = json.loads(response.text)
        print("phone message: ", r)
        if r.get("code") != '0':
            return Response({
                "code": -1,
                "message": "短信发送失败, %s" % r.get("errorMsg")
            })
    member.VERIFICATION_CODE = verification_code
    member.VERIFICATION_CODE_IN_DATE = in_date
    member.save()
    return Response(res)


@api_view(['POST'])
def save_phone_number(request):
    open_id = request.data.get("open_id")
    phone_number = request.data.get("phone_number")
    verification_code = request.data.get("verification_code")
    recommend_id = request.data.get("recommend_id")
    member = models.Member.objects.filter(OPENID=open_id).first()
    if not member:
        return Response({
            "code": -1,
            "message": "用户未授权open id"
        })
    if verification_code != member.VERIFICATION_CODE:
        return Response({
            "code": -1,
            "message": "验证码错误"
        })
    member.PHONE = phone_number
    check_and_set_recommend(open_id, recommend_id, member)
    if member.VERIFICATION_CODE:
        if member.VERIFICATION_CODE_IN_DATE <= datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')):
            return Response({
                "code": -1,
                "message": "验证码已失效"
            })
        else:
            member.VERIFICATION_CODE = None
            member.VERIFICATION_CODE_IN_DATE = None
            member.save()
    else:
        return Response({
            "code": -1,
            "message": "请先发送验证码"
        })
    return Response({
        "code": 0,
        "message": ""
    })


class Phone(APIView):
    pass