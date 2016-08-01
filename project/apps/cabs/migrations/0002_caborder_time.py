# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caborder',
            name='time',
            field=models.DateTimeField(default=None, blank=True),
            preserve_default=False,
        ),
    ]
