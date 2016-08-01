# coding=utf-8

from rest_framework import viewsets, mixins

from apps.api.serializers import passenger
from apps.cabs.models import Passenger

__author__ = 'dragora'


class PassengerViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    # The user model can only be retrieved, listed, updated or created via the API calls
    # User can not delete it's own information
    # So the company decides what information to keep
    serializer_class = passenger.PassengerSerializer
    queryset = Passenger.objects.all()
