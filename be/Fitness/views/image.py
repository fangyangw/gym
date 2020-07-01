# 会员人像
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from Fitness import models
from Fitness.utils import serializer
from rest_framework.decorators import api_view
import base64


@api_view(["GET"])
def get_user_image(request):
    open_id = request.GET.get("open_id")
    member = models.Member.objects.filter(OPENID=open_id).first()
    if member:
        if member.PICTURE and member.PICTURE != '0':
            with member.PICTURE.open("rb") as fh:
                image = fh.read()
                data = "data:image/jpg;base64,%s" % str(base64.b64encode(image), encoding='utf-8')
                return Response({"data": data, "code": 0})
    return Response({"data": "", "code": -1})


class Image(APIView):
    pass