# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('botterdre_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedsong',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 9, 9, 19, 49, 29, 922166)),
        ),
        migrations.AlterField(
            model_name='lyrics',
            name='words',
            field=models.TextField(unique=True),
        ),
    ]
