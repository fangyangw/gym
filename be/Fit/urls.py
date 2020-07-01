"""Fit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from Fitness.views import wx_get
from Fitness.views import course
from Fitness.views import card
from Fitness.views import member
from Fitness.views import image
from Fitness.views import password
from Fitness.views import phone
from Fitness.views import yibi
from Fitness.views import order
from Fitness.views import door_control
from django.contrib import admin
from django.conf.urls import url

"""
前端 ： 101.132.117.242:80
后端 ： 101.132.117.242:443
"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # http://101.132.117.242:8000/index/?code=071Kis3h0yx4Ou1w5l4h0aYr3h0Kis3f
    # 获取用户信息
    path('user_info/', wx_get.GetInfoView.as_view()),
    # 订单接口
    path('pay/', wx_get.GetInfoView.as_view()),
    # # 支付接口
    # path('notify/', wx_get.GetInfoView.as_view()),
    # # 查询订单
    # path('orderquery/', wx_get.GetInfoView.as_view()),

    # 会员信息接口
    path('member/', member.MemberList.as_view()),

    # 课程信息接口
    path('course/', course.CourseList.as_view()),
    # 课程详情接口
    path('course/detail/', course.CourseDetail.as_view()),

    # 会员卡信息列表接口
    path('card/', card.CardList.as_view()),
    # 会员卡详情接口
    path('card/detail/', card.CardDetail.as_view()),

    # 更改密码
    path('password/', password.PassWord.as_view()),
    # 手机号 查询 + 绑定
    path('phone/', phone.Phone.as_view()),
    path('phone/send_verification/', phone.send_verification_code),
    path('phone/save/', phone.save_phone_number),

    # 人脸照片 查看 + 上传
    path('image/', image.Image.as_view()),
    # 易币查询 + 充值
    path('yibi/', yibi.YiBi.as_view()),

    path('yibi/order/', yibi.get_yibi_order),

    path('yibi/buy/', yibi.buy_use_yibi),

    path(r"order/", order.OrderView.as_view(), name="order"),
    path(r"notify/", csrf_exempt(order.PayNotifyView.as_view()), name="notify"),
    path(r"orderquery/", order.OrderQueryView.as_view(), name="orderquery"),

    # app 调用jssdk的签名
    path(r'app/sign/', order.get_app_sign),

    path(r'user/image/', image.get_user_image),
    path(r'user/card/', member.get_user_card),
    path(r'user/course/', member.get_user_course),

    path('door/log/', door_control.DoorControl.as_view({'get': 'list', 'post': 'create'}), name="doorControl")
]
