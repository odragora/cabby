# coding=utf-8

from __future__ import absolute_import

from celery import shared_task

from apps.cabs.bl.orders import issue_order

__author__ = 'dragora'


@shared_task
def order_task(order):
    issue_order(order)