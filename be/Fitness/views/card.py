# 会员卡信息
from rest_framework.views import APIView
from rest_framework.response import Response
from Fitness import models
from Fitness.utils import serializer
from Fitness.views.tools import get_user_discount
from Fit.settings import DICCOUNT_REMARK
import json


class CardList(APIView):
    """
    会员卡列表
    """

    def get(self, request):
        res = {
            'code': 200,
            'data': [],
            'msg': 'Success'
        }
        try:
            data = json.loads(request.query_params.get("params"))
        except:
            data ={}
        open_id = data.get("open_id")
        member = models.Member.objects.filter(OPENID=open_id).first()
        price = get_user_discount(member)
        card_set = models.Card.objects.all()
        card_ser = serializer.CardSerializer(card_set, many=True)
        for item in card_ser.data:
            if item["REMARK"] == DICCOUNT_REMARK:
                item['discount_price'] = price
        res['data'] = card_ser.data
        return Response(res)


"""
{
"CID": "1"
}
"""


class CardDetail(APIView):
    """
    会员卡详情
    """

    def get(self, request):
        return Response('CardDetail')

    def post(self, request):
        res = {
            'code': 200,
            'data': [],
            'msg': 'Success'
        }
        cid = request.data.get('CID')
        if cid:
            card_detail_set = models.Card.objects.filter(CID=cid)
            card_detail_ser = serializer.CardSerializer(card_detail_set, many=True)
            res['data'] = card_detail_ser.data
            return Response(res)
