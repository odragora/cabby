# coding=utf-8

from apps.cabs.models import Cab
from apps.api.serializers.custom import PositionSerializer

__author__ = 'dragora'


class CabSerializer(PositionSerializer):

    class Meta:
        model = Cab
        exclude = ('position',)
        read_only_fields = ('order',)