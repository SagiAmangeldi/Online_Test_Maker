# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPayments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.SmallIntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('payment_type', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.SmallIntegerField(default=100, verbose_name='Balance($)'),
        ),
        migrations.AddField(
            model_name='userpayments',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
