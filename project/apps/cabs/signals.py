# coding=utf-8

from __future__ import absolute_import

from apps.cabs import bl
from apps.cabs.models import CabOrder, OrderTask
from apps.cabs import tasks
from project.celery import app

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

import logging

__author__ = 'dragora'

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CabOrder)
def order_setter(sender, instance, created, **kwargs):
    # Check if the order is a new one
    if created:
        # If the order received has no date assigned we take actions right now
        if not instance.time:
            bl.orders.issue_order(instance)
        # If the time assigned to the order we will delay it's processing
        else:
            # If we will start order processing at the time
            # specified in the order, the cab will be late for sure.
            # That's why we start earlier to be in time.
            # The hardcoded time constant should be replaced with the calculated time
            # based on the traffic jams level and so on.
            prepare_time = settings.ORDERS_SETTINGS['PREPARE_TIME']
            task = tasks.order_task.apply_async(eta=instance.time - prepare_time, kwargs={'order': instance})

            order_task = OrderTask.objects.create(task_id=task.task_id, order=instance)

            log_msg = 'Delayed order id {id} accepted. Time: {time}, destination: {x}, {y}'
            logger.info(log_msg.format(id=instance.id, time=instance.time, x=instance.position.x, y=instance.position.y))


@receiver(post_delete, sender=CabOrder)
def order_revoker(sender, instance, **kwargs):
    # We need to revoke the delayed task when the order is deleted
    task_id = instance.ordertask.task_id
    app.control.revoke(task_id)

    log_msg = 'Order id {id} canceled. Destination: {x}, {y}'
    logger.info(log_msg.format(id=instance.id, x=instance.position.x, y=instance.position.y))