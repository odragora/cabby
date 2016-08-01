# coding=utf-8

from rest_framework import viewsets

from apps.api.serializers import order
from apps.cabs.models import CabOrder

__author__ = 'dragora'


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = order.CabOrderSerializer
    queryset = CabOrder.objects.all()