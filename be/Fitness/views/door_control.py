# 会员信息
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from Fitness import models
from Fitness.utils import serializer
from Fitness.views.tools import get_user_remain_time, activation_card
import logging

logger = logging.getLogger("Door_control")


class DoorControl(ModelViewSet):
    queryset = models.DoorControlLog.objects.all()
    serializer_class = serializer.DoorControlSerializer

    filter_fields = (
        'id', 'id'
    )

    def create(self, request, *args, **kwargs):
        response = super(DoorControl, self).create(request, *args, **kwargs)
        try:
            mid = request.data.get("userID")
            member = models.Member.objects.filter(MID=mid).first()
            if member:
                user_cards = models.UserCard.objects.filter(MEMBER_ID=member)
                remain_day, card = get_user_remain_time(member)
                if card and card.ACTIVATION_DATE is None:
                    activation_card(card)
        except Exception as e:
            logger.error(str(e))
        return response

    def get_serializer(self, *args, **kwargs):
        return super(DoorControl, self).get_serializer(*args, **kwargs)

    class Meta:
        model = models.DoorControlLog
