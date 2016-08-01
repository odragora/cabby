from django.contrib.gis.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from django.utils import timezone


def validate_datetime(value):
    if value > timezone.now() + settings.ORDERS_SETTINGS['MAX_TIME']:
        raise ValidationError('Order estimated time should fit the daily time frame. Time provided: {}'.format(value))


class Passenger(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class CabOrder(models.Model):
    position = models.PointField()
    time = models.DateTimeField(blank=True, null=True, validators=[validate_datetime])
    passenger = models.ForeignKey(to=Passenger)

    def __unicode__(self):
        return '{x}, {y} at {time}'.format(x=self.position.x, y=self.position.y, time=self.time)


class OrderTask(models.Model):
    task_id = models.IntegerField()
    order = models.OneToOneField(to=CabOrder)

    def __unicode__(self):
        return self.task_id


class Cab(models.Model):
    position = models.PointField()
    order = models.OneToOneField(to=CabOrder, blank=True, null=True, on_delete=models.SET_NULL)

    objects = models.GeoManager()

    def __unicode__(self):
        return '{x}, {y}'.format(x=self.position.x, y=self.position.y)