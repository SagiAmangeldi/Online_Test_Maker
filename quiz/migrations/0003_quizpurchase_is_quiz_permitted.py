# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20151013_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizpurchase',
            name='is_quiz_permitted',
            field=models.BooleanField(default=False),
        ),
    ]
