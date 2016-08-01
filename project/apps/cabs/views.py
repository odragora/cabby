from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic import TemplateView

from apps.cabs import tasks

# Create your views here.


class TestView(TemplateView):
    def get(self, request, *args, **kwargs):

        # res = tasks.test.apply_async(countdown=5, kwargs={'msg': 'Hello!'})
        # # tasks.test.delay(msg='Hello!')
        # print 'Res get():', res.get()

        return render(request, template_name='test.html')