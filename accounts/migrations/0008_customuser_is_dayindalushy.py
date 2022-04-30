# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151228_0744'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_dayindalushy',
            field=models.BooleanField(default=False),
        ),
    ]
