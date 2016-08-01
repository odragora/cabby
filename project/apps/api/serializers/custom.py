# coding=utf-8

from rest_framework import serializers
from django.contrib.gis.geos import Point

__author__ = 'dragora'


class PositionSerializer(serializers.HyperlinkedModelSerializer):

    pos_x = serializers.FloatField(write_only=True)
    pos_y = serializers.FloatField(write_only=True)

    class Meta:
        abstract = True

    def to_internal_value(self, data):
        data_internal = super(PositionSerializer, self).to_internal_value(data)
        pos_x = data_internal.pop('pos_x')
        pos_y = data_internal.pop('pos_y')
        data_internal['position'] = Point(pos_x, pos_y)
        return data_internal

    def to_representation(self, instance):
        representation = super(PositionSerializer, self).to_representation(instance)
        representation['pos_x'] = instance.position.x
        representation['pos_y'] = instance.position.y
        return representation