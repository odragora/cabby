# coding=utf-8

from django.apps import AppConfig

__author__ = 'dragora'


class CabsConfig(AppConfig):

    name = 'apps.cabs'
    verbose_name = 'Cabs'

    def ready(self):

        import signals