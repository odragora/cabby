# coding=utf-8

from rest_framework import serializers

from apps.cabs.models import Passenger

__author__ = 'dragora'


class PassengerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Passenger