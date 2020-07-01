from django.views.generic import View
# from login
from Fit import settings
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from Fitness.views.WechatAPI import WechatLogin
from Fitness.utils import wechatConfig
from Fitness.utils import serializer
from Fitness import models
from Fit.settings import IS_ON_SALE, FREE_DAY
import requests
import json
import time
import datetime
import re


class WechatViewSet(View):
    wechat_api = WechatLogin()


class GetInfoView(APIView):
    def get(self, request):
        res = {
            'code': 200,
            'data': [],
            'msg': 'success'
        }

        # 微信内置浏览器获取access_token微信接口
        access_token_url = wechatConfig.defaults['wechat_browser_access_token']
        # 微信内置浏览器获取用户信息微信接口
        user_info_url = wechatConfig.defaults['wechat_browser_user_info']

        # 微信内置浏览器获取用户信息微信接口
        app_user_info_url = wechatConfig.defaults['app_user_info']
        # 前端获取code
        code = request.GET.get('code')
        openid = request.GET.get("open_id")
        access_token = None
        print(code, openid)
        if not openid:
            # 首先查看数据库是否存在code
            code_set = models.CodeToAccess.objects.filter(CODE=code)
            # 存在直接获取access_token
            if code_set:
                code_ser = serializer.CodeAccessSerializer(code_set, many=True)
                access_token = code_ser.data[0]['ACCESS_TOKEN']
                openid = code_ser.data[0]['OPEN_ID']
            # 不存在通过回调地址获取access_token
            else:
                # 获取access_token
                url_access_token = access_token_url + '?appid={APPID}&secret={SECRET}&code={CODE}&grant_type=authorization_code'.format(
                    APPID=settings.AppID, SECRET=settings.AppSecret, CODE=code)
                data1 = requests.get(url_access_token)
                access_dict = json.loads(data1.text)
                print(access_dict)
                if access_dict.get('errcode'):
                    res['code'] = access_dict['errcode']
                    res['msg'] = access_dict['errmsg']
                    print('error code')
                    return Response(res)

                access_token = access_dict.get('access_token')
                openid = access_dict.get('openid')
                print(access_token)
                print(openid)

                # 存入数据库
                models.CodeToAccess.objects.create(
                    CODE=code,
                    ACCESS_TOKEN=access_token,
                    OPEN_ID=openid
                )
                print(666)
        # 存入数据库
        user_profile = models.UserProfile.objects.filter(openid=openid).first()
        if not user_profile:
            user_profile = models.UserProfile(
                openid=openid,
            )
        if access_token:
            user_profile.accesstoken = access_token
        user_profile.save()
        # 获取user_info
        time.sleep(0.5)
        token = models.Config.objects.filter(key="access_token").first()
        url_user_info = app_user_info_url + '?openid={OPENID}&access_token={ACCESS_TOKEN}&lang=zh_CN'.format(
                OPENID=openid, ACCESS_TOKEN=token.value)
        data2 = requests.get(url_user_info)
        data2.encoding = 'utf-8'
        user_dict = json.loads(data2.text)
        print("-=-", user_dict)
        if user_dict.get('errcode'):
            res['code'] = user_dict['errcode']
            res['msg'] = user_dict['errmsg']
            return Response(res)
        # 更新用户数据库
        # models.UserProfile.objects.filter(openid=user_dict['openid']).update(
        #     nickname=user_dict.get('nickname').encode('iso-8859-1').decode('utf-8'),
        #     wsex=user_dict.get('sex'),
        #     headimgurl=user_dict.get('headimgurl'),
        # )
        nickname = user_dict.get('nickname')

        sex = user_dict.get('sex')
        headimgurl = user_dict.get('headimgurl')
        city = user_dict.get('city', '')
        user_profile.subscribe = user_dict.get("subscribe", 0)
        province = user_dict.get('province', '')
        if user_dict.get("subscribe", 0) != 1:
            url_user_info = user_info_url + '?access_token={ACCESS_TOKEN}&openid={OPENID}&lang=zh_CN'.format(
            ACCESS_TOKEN=user_profile.accesstoken, OPENID=openid)
            data2 = requests.get(url_user_info)
            user_dict = json.loads(data2.text)
            print("---", user_dict)
            if user_dict.get('errcode'):
                res['code'] = user_dict['errcode']
                res['msg'] = user_dict['errmsg']
                return Response(res)
            nickname = user_dict.get('nickname').encode('iso-8859-1').decode('utf-8')
            sex = user_dict.get('sex')
            headimgurl = user_dict.get('headimgurl')
            city = user_dict.get('city', '').encode('iso-8859-1').decode('utf-8')
            province = user_dict.get('province', '').encode('iso-8859-1').decode('utf-8')
        user_profile.nickname = nickname
        user_profile.wsex = sex
        user_profile.headimgurl = headimgurl
        user_profile.city = city
        user_profile.province = province
        user_profile.save()
        # 同步会员数据表
        member = models.Member.objects.filter(OPENID=user_dict['openid']).first()
        if not member:
            member = models.Member(
                OPENID=user_dict['openid'],
                NICK=nickname,
                PHOTO=headimgurl
            )

        member.NICK = nickname
        member.PHOTO = headimgurl
        member.save()
        user_set = models.UserProfile.objects.filter(openid=user_dict['openid'])
        user_ser = serializer.UserProfileSerializer(user_set, many=True)
        res['data'] = user_ser.data[0]
        return Response(res)


def update_token():
    app_access_token_url = wechatConfig.defaults['app_access_token']
    app_url_access_token = app_access_token_url + '?appid={APPID}&secret={SECRET}&grant_type=client_credential'.format(
        APPID=settings.AppID, SECRET=settings.AppSecret)
    data1 = requests.get(app_url_access_token)
    access_dict1 = json.loads(data1.text)
    if access_dict1.get('errcode'):
        print('error code')
    access_token = access_dict1.get("access_token")

    # get jsapi ticket
    get_jsapi_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % access_token
    response = requests.request("GET", get_jsapi_url)
    r = json.loads(response.text)
    jsapi_ticket = None
    if r.get("errcode") == 0:
        jsapi_ticket = r.get("ticket")
    token = models.Config.objects.filter(key="access_token").first()
    if not token:
        token = models.Config(key="access_token", value=access_token)
    token.value = access_token
    token.save()
    jsapi = models.Config.objects.filter(key="jsapi_ticket").first()
    if not jsapi:
        jsapi = models.Config(key="jsapi_ticket", value=jsapi_ticket)
    jsapi.value = jsapi_ticket
    jsapi.save()

"""
code 换取 access_token 的值
access_dict = {
    'access_token': '33_uKHsXHTuFNU2qFxPRU_Z8e4-_i4OLPhAorqSB9BSAbfNF6Dce9Ix8AlCu9SpJhdFRb9TLg-7-qXQsxFsKlsqcA',
    'expires_in': 7200,
    'refresh_token': '33_OD0XgYLpz5ca7htm-sCagYCLtCBktp6NzMZkmVy52l6aHusAlB6eLIUhnMurDrn53HxFJEosu8t0mlFBxF9HIA',
    'openid': 'o6IrivxChcIxmzrUu4JkCmaNV6tg', 
    'scope': 'snsapi_userinfo'
}
access_token 换取 user_info 的值
user_dict = {
    'openid': 'o6IrivxChcIxmzrUu4JkCmaNV6tg',
    'nickname': '1',
    'sex': 1,
    'language': 'zh_CN',
    'city': '',
    'province': 'è¿ªæ\x8b\x9c',
    'country': 'é\x98¿æ\x8b\x89ä¼¯è\x81\x94å\x90\x88é\x85\x8bé\x95¿å\x9b½',
    'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ4P3Fo9PSbFzXz3a1Sjr9T8HvIOmuFTgJbPNaPYL8g9Q6Oj62vex7afXbegv9qFn9PhqKQD6ialjQ/132',
    'privilege': []
}
"""
