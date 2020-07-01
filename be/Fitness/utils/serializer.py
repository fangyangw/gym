from rest_framework import serializers
from Fitness import models


class OrderSerialzier(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    out_trade_no = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    微信用户序列化
    """

    class Meta:
        model = models.UserProfile
        fields = (
            'openid', 'nickname', 'wsex', 'headimgurl'
        )
        depth = 0


class MemberSerializer(serializers.ModelSerializer):
    """
    会员信息序列化
    """

    class Meta:
        model = models.Member
        fields = (
            'MID', 'NICK', 'PHOTO', 'PHONE', 'PICTURE', 'CARD_ID', 'COURSE_ID', 'YIBI', 'SHARE', 'REMAIN_TIME', 'register_door_control_status'
        )
        depth = 0

class CourseSerializer(serializers.ModelSerializer):
    """
    健身课程序列化
    """
    STORE_NAME = serializers.CharField(source='STORE_ID.NAME', read_only=True)
    COACH_NAME = serializers.CharField(source='COACH_ID.NAME', read_only=True)
    COACH_PHOTO = serializers.ImageField(source='COACH_ID.PHOTO', read_only=True)

    class Meta:

        model = models.Course
        fields = (
            'CID', 'NAME', 'STORE_ID', 'TYPE', 'COACH_ID', 'DISCOUNTS', 'DURATION', 'PRICE', 'SYNOPSIS', 'BACKGROUND',
            'REMAIN_QUANTITY', 'STORE_NAME', 'COACH_NAME', 'COACH_PHOTO', 'COURSE_DETAIL_PICTURE'
        )
        depth = 0


class CardSerializer(serializers.ModelSerializer):
    """
    会员卡信息序列化
    """

    class Meta:
        model = models.Card
        fields = (
            'CID', 'NAME', 'TYPE', 'REMARK', 'INDATE', 'PRICE', 'DAYS', 'STORE_ID', 'REMAIN_QUANTITY'
        )
        depth = 0


class StoreSerializer(serializers.ModelSerializer):
    """
    门店信息序列化
    """

    class Meta:
        model = models.Store
        fields = (
            'SID', 'NAME', 'ADDRESS'
        )
        depth = 0


class CoachSerializer(serializers.ModelSerializer):
    """
    健身教练信息序列化
    """

    class Meta:
        model = models.Coach
        fields = (
            'CID', 'NAME', 'STORE_ID', 'PHOTO'
        )
        depth = 0


class CodeAccessSerializer(serializers.ModelSerializer):
    """
    微信用户序列化
    """

    class Meta:
        model = models.CodeToAccess
        fields = (
            'CODE', 'ACCESS_TOKEN', 'OPEN_ID'
        )
        depth = 0


class DoorControlSerializer(serializers.ModelSerializer):
    """
    微信用户序列化
    """
    required_formats = ['%Y-%m-%d %H:%M:%S']
    date = serializers.DateTimeField(input_formats=required_formats)

    class Meta:
        model = models.DoorControlLog
        fields = (
            'userID', 'verifyMode', 'date'
        )
        depth = 0


class UserCardSerializer(serializers.ModelSerializer):
    NAME = serializers.CharField(source='CARD_ID.NAME', read_only=True)
    TYPE = serializers.CharField(source='CARD_ID.TYPE', read_only=True)
    INDATE = serializers.CharField(source='CARD_ID.INDATE', read_only=True)

    class Meta:
        model = models.UserCard
        fields = (
            'ACTIVATION_DATE', 'EXPIRATION_TIME', 'TYPE', 'NAME', 'INDATE'
        )
        depth = 0


class UserCourseSerializer(serializers.ModelSerializer):
    NAME = serializers.CharField(source='COURSE_ID.NAME', read_only=True)
    TYPE = serializers.CharField(source='COURSE_ID.TYPE', read_only=True)
    DURATION = serializers.CharField(source='COURSE_ID.DURATION', read_only=True)
    BACKGROUND = serializers.CharField(source='COURSE_ID.BACKGROUND', read_only=True)

    class Meta:
        model = models.UserCourse
        fields = (
            'ACTIVATION_DATE', 'EXPIRATION_TIME', 'NAME', 'TYPE', 'DURATION', "BACKGROUND"
        )
        depth = 0


class YibiOrderSerializer(serializers.ModelSerializer):
    required_formats = ['%Y-%m-%d %H:%M:%S']
    update_time = serializers.DateTimeField(input_formats=required_formats)

    class Meta:
        model = models.YibiOrder
        fields = (
            'description', 'total_yibi', 'create_time', 'update_time',
            'status', 'payee', 'payer', 'other_id', 'trade_type'
        )
        depth = 0
