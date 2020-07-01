from django.contrib import admin
from django.contrib.admin import decorators
from Fitness.models import UserProfile, Member, Order, Card, Course, YibiOrder, Coach, UserCard, UserCourse
from django.utils.safestring import mark_safe
# Register your models here.


@decorators.register(UserProfile)
class UserProfileControl(admin.ModelAdmin):
    list_display = ("nickname", "subscribe")


@decorators.register(Member)
class UserProfileControl(admin.ModelAdmin):
    list_display = ("MID", "NICK", "PHONE", "YIBI", "user_picture")

    def user_picture(self, obj):
        try:
            img = mark_safe('<img src="%s" width="50px" />' % ("https://www.ezaifit.top:80/"+obj.PICTURE.url.split("Fit/")[-1],))
        except Exception as e:
            img = ''
        return img
    user_picture.short_description = '人脸图片'
    user_picture.allow_tags = True


admin.site.register([Order, Card, Course, YibiOrder, Coach, UserCard, UserCourse])
