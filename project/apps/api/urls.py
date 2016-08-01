# coding=utf-8

from rest_framework.routers import DefaultRouter

from views import order, cab, passenger

__author__ = 'dragora'

router = DefaultRouter()
router.register(r'orders', order.OrderViewSet)
router.register(r'cabs', cab.CabViewSet)
router.register(r'passengers', passenger.PassengerViewSet)
urlpatterns = router.urls