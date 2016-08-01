# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.cabs.models


class Migration(migrations.Migration):

    dependencies = [
        ('cabs', '0002_caborder_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='caborder',
            name='time',
            field=models.DateTimeField(blank=True, validators=[apps.cabs.models.validate_datetime]),
        ),
        migrations.AddField(
            model_name='caborder',
            name='passenger',
            field=models.ForeignKey(default=None, to='cabs.Passenger'),
            preserve_default=False,
        ),
    ]
