# coding=utf-8

from apps.cabs.models import CabOrder
from apps.api.serializers.custom import PositionSerializer

__author__ = 'dragora'


class CabOrderSerializer(PositionSerializer):

    class Meta:
        model = CabOrder
        fields = ('time', 'pos_x', 'pos_y', 'passenger', 'url')
        read_only_fields = ('cab',)