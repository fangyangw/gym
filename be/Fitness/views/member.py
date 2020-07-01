# 会员信息
from rest_framework.views import APIView
from rest_framework.response import Response
from Fitness import models
from Fitness.utils import serializer
import requests
from Fit.settings import MEDIA_ROOT, FREE_CARD_NAME, FREE_DAY
import os
import uuid
from Fitness.utils.door_control import check_and_register
from Fitness.views.yibi import check_and_finish_recommend, check_and_set_free_data
from Fitness.views.tools import get_user_remain_time
import base64
import datetime
import logging
import pytz
from rest_framework.decorators import api_view
from django.db.models import Q


logger = logging.getLogger("MemberView")


class MemberList(APIView):
    """
    会员列表
    """

    def get(self, request):
        res = {
            'code': 200,
            'data': [],
            'msg': 'Success'
        }
        try:
            open_id = request.GET.get('OPENID')
            print(request.get_full_path())
            member_set = models.Member.objects.filter(OPENID=open_id)
            member = member_set.first()
            class_count = models.UserCourse.objects.filter(MEMBER_ID=member).count()
            card_count = models.UserCard.objects.filter(MEMBER_ID=member).filter(~Q(REMARK=FREE_CARD_NAME)).count()
            member_ser = serializer.MemberSerializer(member_set, many=True)
            res['data'] = member_ser.data
            res['total_card'] = card_count
            res['total_class'] = class_count
            recommend_info = {}
            if member.SHARE and member.SHARE != '0':
                recommend_member = models.Member.objects.filter(OPENID=member.SHARE).first()
                if recommend_member:
                    recommend_info['NICK'] = recommend_member.NICK
                    recommend_info['PHOTO'] = recommend_member.PHOTO
                    recommend_info["OPENID"] = recommend_member.OPENID
            res['recommend_member'] = recommend_info
            shared_members = []
            shared_set = models.Member.objects.filter(SHARE=member.OPENID)
            if bool(shared_set):
                for shared_member in shared_set:
                    shared_members.append({
                        "NICK": shared_member.NICK,
                        "PHOTO": shared_member.PHOTO,
                        "OPENID": shared_member.OPENID
                    })
            user = models.UserProfile.objects.filter(openid=open_id).first()
            res["subscribe"] = 0
            res["REMAIN_TIME"] = get_user_remain_time(member)[0]
            if user:
                res["subscribe"] = user.subscribe
            res['shared_members'] = shared_members
            return Response(res)
        except Exception as e:
            res['code'] = 500
            res['msg'] = e
            return Response(res)

    def post(self, request):
        open_id = request.data.get("open_id")
        member = models.Member.objects.filter(OPENID=open_id).first()
        user = models.UserProfile.objects.filter(openid=open_id).first()
        if not member or not user:
            return Response({
                'code': 500,
                'message': "%s user not exists" % open_id
            })
        password = request.data.get("password")
        if password:
            member.PASSWORD = password
        recommend_id = request.data.get("recommend_id")
        try:
            check_and_set_recommend(open_id, recommend_id, member)
        except Exception as e:
            logger.error("Set recommend error, %s" % str(e))
        # with member.PICTURE.open('rb') as f:
        #     image = f.read()
        #     image_base64 = str(base64.b64encode(image), encoding='utf-8')

        server_id = request.data.get("server_id")
        access_token = models.Config.objects.filter(key="access_token").first()
        url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (access_token.value, server_id)
        if server_id:
            user_door_log = models.DoorControlLog.objects.filter(userID=str(member.MID)).first()
            if user_door_log:
                return Response({
                    'code': 500,
                    'message': "已经使用人脸开门后，照片不允许修改，如需更换请联系管理员。"
                })
            response = requests.request("GET", url)
            img = response.content
            image_name = os.path.join(MEDIA_ROOT, str(uuid.uuid4()) + ".jpg")
            with open(image_name, 'wb') as fh:
                fh.write(img)
            if response:
                member.PICTURE = image_name
        member.save()
        try:
            check_and_register(member)
        except Exception as e:
            print("Error: setup to door control error! %s" % str(e))
        member_ser = serializer.MemberSerializer(member)
        return Response(member_ser.data)

    # def get_remain_time(self, request):
    #     open_id = request.GET.get('OPENID')
    #     member = models.Member.objects.filter(OPENID=open_id).first()
    #     res = {
    #         'code': 200,
    #         "remain_days": int(member.REMAIN_TIME),
    #         "remain_in": True if int(member.REMAIN_TIME) > 0 else False,
    #         'msg': 'Success'
    #     }
    #     return res


def check_and_set_recommend(open_id, recommend_id, member):
    if recommend_id:
        shared = models.Member.objects.filter(SHARE=open_id).first()
        if member.SHARE and member.SHARE != '0':
            print("Warning: have be shared")
        else:
            # have shared to people, cannot be shared
            if shared:
                print("Warning: have shared to people, cannot be shared.")
            else:
                print("A new member")
                share_member = models.Member.objects.filter(OPENID=recommend_id).first()
                if share_member:
                    member.SHARE = recommend_id
                    member.save()
                else:
                    print("Warning: share member is not exists.")
        check_and_finish_recommend(member, recommend_id)
    check_and_set_free_data(member)


@api_view(['GET'])
def get_user_card(request):
    open_id = request.GET.get("open_id")
    member = models.Member.objects.filter(OPENID=open_id).first()
    res = {
        'code': 200,
        'data': [],
        'msg': 'Success'
    }
    if member:
        card_set = models.UserCard.objects.filter(MEMBER_ID=member).filter(~Q(REMARK=FREE_CARD_NAME))
        card_data = serializer.UserCardSerializer(data=card_set, many=True)
        card_data.is_valid()
        res['data'] = card_data.data
    return Response(res)


@api_view(['GET'])
def get_user_course(request):
    open_id = request.GET.get("open_id")
    member = models.Member.objects.filter(OPENID=open_id).first()
    res = {
        'code': 200,
        'data': [],
        'msg': 'Success'
    }
    if member:
        course_set = models.UserCourse.objects.filter(MEMBER_ID=member)
        course_data = serializer.UserCourseSerializer(data=course_set, many=True)
        course_data.is_valid()
        res['data'] = course_data.data
    return Response(res)
