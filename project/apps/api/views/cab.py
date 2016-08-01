# coding=utf-8

from rest_framework import viewsets

from apps.api.serializers import cab
from apps.cabs.models import Cab

__author__ = 'dragora'


class CabViewSet(viewsets.ModelViewSet):
    serializer_class = cab.CabSerializer
    queryset = Cab.objects.all()