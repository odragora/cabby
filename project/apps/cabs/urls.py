# coding=utf-8

from django.conf.urls import include, url, patterns

import views
__author__ = 'dragora'

urlpatterns = [
    url(r'^$', views.TestView.as_view())
]