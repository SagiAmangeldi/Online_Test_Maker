# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151205_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
