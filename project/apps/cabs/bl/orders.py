# coding=utf-8

from django.core.exceptions import ObjectDoesNotExist

from apps.cabs.models import Cab

import logging

__author__ = 'dragora'

logger = logging.getLogger(__name__)


def get_log_msgs():
    return {
        'SUCCESS': """
Cab order id {order_id}: issued to the cab id {cab_id}. Destination: {x}, {y}""",
        'NO_CABS': """
Cab order id {order_id}: can\'t issue the order (no cabs available). Destination: {x}, {y}"""
    }


def issue_order(order):
    # Find the nearest cab without any active order at the moment
    try:
        closest_cab = Cab.objects.distance(order.position).order_by('distance').filter(order=None)[0]
        # Set the order instance to the cab `order` field
        closest_cab.order = order
        closest_cab.save()

        log_msg = get_log_msgs()['SUCCESS']
        logger.info(
            log_msg.format(order_id=order.id, cab_id=closest_cab.id)
        )
        # TODO: inform the customer that the cab is going to pick him up
    except ObjectDoesNotExist:
        log_msg = get_log_msgs()['NO_CABS']
        logger.info(
            log_msg.format(order_id=order.id)
        )
        # TODO: inform the customer that there are not any cabs able to pick him up