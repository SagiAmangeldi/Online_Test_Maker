# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151211_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.SmallIntegerField()),
                ('comment', models.CharField(max_length=80)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='quizpayment',
            options={},
        ),
    ]
