# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20151015_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionattempt',
            name='attemptdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 24, 19, 11, 47, 250228, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='questionattempt',
            name='answer',
            field=models.ForeignKey(default=1, to='quiz.Answer'),
            preserve_default=False,
        ),
    ]
