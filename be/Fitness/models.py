from django.db import models

# Create your models here.
class DoorControlLog(models.Model):
    """
    door control log
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='id')
    userID = models.CharField('userID', max_length=100, null=True, blank=True)
    verifyMode = models.CharField('verifyMode', max_length=100, null=True, blank=True)
    date = models.DateTimeField('date', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "door_control_log"
        db_table = verbose_name
        verbose_name_plural = "门禁日志表"


class Config(models.Model):
    key = models.CharField('key', primary_key=True, max_length=100)
    value = models.CharField('value', max_length=512)

    class Meta:
        verbose_name = "config"
        db_table = verbose_name
        verbose_name_plural = "配置文件表"

# Create your models here.
class CodeToAccess(models.Model):
    """
    Code_To_Access
    """
    CAID = models.AutoField(auto_created=True, primary_key=True, verbose_name='CA')
    CODE = models.CharField('Code', max_length=100, null=True, blank=True)
    ACCESS_TOKEN = models.CharField('Access', max_length=512, null=True, blank=True)
    OPEN_ID = models.CharField('OpenID', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "06_code_access_table"
        db_table = verbose_name
        verbose_name_plural = "用户授权token表"


class UserProfile(models.Model):
    user = models.OneToOneField('Member', on_delete=models.CASCADE, null=True, default=None)
    # 微信开发
    accesstoken = models.CharField("微信 access_token", max_length=512, default='')
    openid = models.CharField("微信 openid", max_length=32, default='')
    nickname = models.CharField("微信昵称", max_length=256, default='')
    wsex = models.CharField("微信性别", max_length=3, default='')
    province = models.CharField("微信省份", max_length=50, default='')
    city = models.CharField("微信城市", max_length=50, default='')
    country = models.CharField("微信国家", max_length=50, default='')
    headimgurl = models.CharField("微信头像", max_length=200, default='')
    privilege = models.CharField("微信权限", max_length=3, default='')
    unionid = models.CharField("微信 unionid", max_length=32, default='')
    refresh_token = models.CharField("微信 refresh_token", max_length=512, default='')
    refresh_token_time = models.IntegerField(default=0)
    subscribe = models.IntegerField("公众号关注状态", default=0)
    jsapi_ticket = models.CharField("微信 jsapi_ticket", max_length=512, default=None)

    class Meta:
        verbose_name = "00_user_table"
        db_table = verbose_name
        verbose_name_plural = "用户扩展信息表"


class Member(models.Model):
    """
    会员信息表
    """
    MID = models.AutoField(auto_created=True, primary_key=True, verbose_name='会员ID')
    OPENID = models.CharField("微信openid", max_length=64, default='')
    PASSWORD = models.CharField('支付密码', max_length=255, blank=True, null=True)
    NICK = models.CharField('昵称', max_length=100, null=True, blank=True)
    PHOTO = models.CharField('头像', null=True, blank=True, max_length=512)
    PHONE = models.CharField('手机号', max_length=100, null=True, blank=True, default='0')
    PICTURE = models.ImageField('人脸照片', null=True, blank=True, upload_to='upload/', default='0')
    CARD_ID = models.ForeignKey('Card', default='', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='卡ID')
    COURSE_ID = models.ForeignKey('Course', default='', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='课程ID')
    YIBI = models.CharField('我的易币', max_length=100, null=True, blank=True, default='0')
    SHARE = models.CharField('我的分享', max_length=100, null=True, blank=True, default='0')
    REGISTER_DATE = models.DateField("注册时间", auto_now_add=True)
    REMAIN_TIME = models.CharField('会员剩余时间', max_length=100, null=True, blank=True, default='0')
    VERIFICATION_CODE = models.CharField("验证码", max_length=64, default='', null=True, blank=True)
    VERIFICATION_CODE_IN_DATE = models.DateTimeField("验证码有效时间", default=None, null=True, blank=True)
    register_door_control_status = models.BooleanField("注册门禁人脸识别状态", default=False)
    notice_status = models.BooleanField("微信提醒状态", default=False)

    class Meta:
        verbose_name = "01_member_table"
        db_table = verbose_name
        verbose_name_plural = "会员信息表"


class Course(models.Model):
    """
    课程表
    """
    CID = models.AutoField(auto_created=True, primary_key=True, verbose_name='课程ID')
    NAME = models.CharField('课程名称', max_length=100, null=True, blank=True)
    STORE_ID = models.ForeignKey('Store', verbose_name='门店ID', null=True, blank=True, on_delete=models.SET_NULL)
    TYPE = models.CharField('课程类型', max_length=100, null=True, blank=True)
    COACH_ID = models.ForeignKey('Coach', verbose_name='教练ID', null=True, blank=True, on_delete=models.SET_NULL)
    DISCOUNTS = models.CharField('优惠信息', max_length=100, null=True, blank=True)
    DURATION = models.CharField('持续时长', max_length=100, null=True, blank=True)
    PRICE = models.CharField('售价', max_length=100, null=True, blank=True)
    SYNOPSIS = models.CharField('简介', max_length=100, null=True, blank=True)
    REMAIN_QUANTITY = models.CharField('剩余数量', max_length=100, null=True, blank=True)
    COURSE_DETAIL = models.TextField("课程详情", null=True, blank=True)
    COURSE_DETAIL_PICTURE = models.ImageField('课程详情图片', null=True, blank=True, upload_to='picture/static_picture/course_detail/')
    BACKGROUND = models.ImageField('背景图', null=True, blank=True, upload_to='picture/static_picture/background/')
    DAYS = models.IntegerField('有效天数', null=True, blank=True, default=0)

    class Meta:
        verbose_name = "02_course_table"
        db_table = verbose_name
        verbose_name_plural = "课程表"


class Card(models.Model):
    """
    会员卡表
    """
    CID = models.AutoField(auto_created=True, primary_key=True, verbose_name='卡ID')
    NAME = models.CharField('卡名称', max_length=100, null=True, blank=True)
    # 月卡 半年卡 。。。
    TYPE = models.CharField('卡类型', max_length=100, null=True, blank=True)
    # 预售卡，初次到店开始计算
    REMARK = models.CharField('备注', max_length=255, null=True, blank=True)
    INDATE = models.CharField('有效期', max_length=255, null=True, blank=True)
    PRICE = models.CharField('售价', max_length=100, null=True, blank=True)
    DAYS = models.CharField('天数', max_length=100, null=True, blank=True)
    STORE_ID = models.ForeignKey('Store', verbose_name='门店ID', null=True, blank=True, on_delete=models.SET_NULL)
    REMAIN_QUANTITY = models.CharField('剩余数量', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "03_card_table"
        db_table = verbose_name
        verbose_name_plural = "会员卡表"


class UserCard(models.Model):
    """
    用户的会员卡表
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='id')
    REMARK = models.CharField('备注', max_length=255, null=True, blank=True)
    ACTIVATION_DATE = models.DateTimeField(null=True, blank=True, verbose_name="激活日期")
    EXPIRATION_TIME = models.DateTimeField('会员到期时间', null=True, blank=True, default=None)
    CARD_ID = models.ForeignKey('Card', verbose_name='卡ID', null=True, blank=True, on_delete=models.SET_NULL)
    MEMBER_ID = models.ForeignKey('Member', verbose_name='用户ID', null=True, blank=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "user_card"
        db_table = verbose_name
        verbose_name_plural = "用户的会员卡表"


class UserCourse(models.Model):
    """
    用户的课程表
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='id')
    REMARK = models.CharField('备注', max_length=255, null=True, blank=True)
    ACTIVATION_DATE = models.DateTimeField(null=True, blank=True, verbose_name="激活日期")
    EXPIRATION_TIME = models.DateTimeField('会员到期时间', null=True, blank=True, default=None)
    REMAIN_COURSE = models.DateTimeField('剩余课时', null=True, blank=True, default=None)
    COURSE_ID = models.ForeignKey('Course', verbose_name='课程ID', null=True, blank=True, on_delete=models.SET_NULL)
    MEMBER_ID = models.ForeignKey('Member', verbose_name='用户ID', null=True, blank=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "user_course"
        db_table = verbose_name
        verbose_name_plural = "用户的课程表"


class Store(models.Model):
    """
    店铺表
    """
    SID = models.AutoField(auto_created=True, primary_key=True, verbose_name='门店ID')
    NAME = models.CharField('门店名称', max_length=100, null=True, blank=True)
    ADDRESS = models.CharField('门店地址', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "04_store_table"
        db_table = verbose_name
        verbose_name_plural = "店铺表"


class Coach(models.Model):
    """
    教练表
    """
    CID = models.AutoField(auto_created=True, primary_key=True, verbose_name='门店ID')
    NAME = models.CharField('姓名', max_length=100, null=True, blank=True)
    PHOTO = models.ImageField('教练的图片', null=True, blank=True, upload_to='picture/static_picture/coach_photo/')
    STORE_ID = models.ForeignKey('Store', verbose_name='门店ID', null=True, blank=True, on_delete=models.SET_NULL)

    # COURSE_ID = models.ForeignKey('Course', verbose_name='课程ID', on_delete=models.SET_NULL, null=True, blank=True,)
    class Meta:
        verbose_name = "05_coach_table"
        db_table = verbose_name
        verbose_name_plural = "教练表"


class Order(models.Model):
    """
    订单表
    """
    prepay_id = models.CharField(max_length=64, null=True, blank=True, verbose_name="预支付交易会话标识")
    out_trade_no = models.CharField(max_length=64, null=True, blank=True, verbose_name="商户订单号")
    transaction_id = models.CharField(max_length=64, null=True, blank=True, verbose_name="微信支付订单号")
    bank_type = models.CharField(max_length=64, null=True, blank=True, verbose_name="付款银行")
    cash_fee = models.IntegerField(null=True, blank=True, verbose_name="现金支付金额")
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="支付完成时间")
    busname = models.CharField(max_length=16, null=True, blank=True, verbose_name="业务")
    description = models.TextField(verbose_name="商品描述")
    total_fee = models.IntegerField(verbose_name="订单总金额", help_text="订单总金额，单位分")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    good_id = models.IntegerField(verbose_name="商品id")
    open_id = models.CharField(max_length=64, verbose_name="用户微信openid")

    class Meta:
        verbose_name = "07_Order_table"
        db_table = verbose_name
        verbose_name_plural = "订单表"


class YibiOrder(models.Model):
    """
    易币交易表
        trade_type:  rewards_from_share, trade
        description
        create_time
        update_time
        total_yibi
        payer:   分享所得的支付方为：SYSTEM
        payee:
        id:
        status:
        other_id:  用于记录被分享人的id
    """
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='id')
    description = models.TextField(verbose_name="商品描述")
    total_yibi = models.IntegerField(verbose_name="订单总金额", help_text="订单总金额，单位易币个数")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    payee = models.CharField(max_length=64, verbose_name="收款方")
    payer = models.CharField(max_length=64, verbose_name="支付方")
    other_id = models.CharField(max_length=64, verbose_name="其他id")
    trade_type = models.CharField(max_length=64, verbose_name="交易类型")
    good_id = models.IntegerField(verbose_name="商品id")
    busname = models.CharField(max_length=16, null=True, blank=True, verbose_name="业务")

    class Meta:
        verbose_name = "yibi_order"
        db_table = verbose_name
        verbose_name_plural = "易币交易表"
