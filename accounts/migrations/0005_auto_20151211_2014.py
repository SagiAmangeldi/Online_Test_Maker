# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20151205_1032'),
        ('accounts', '0004_auto_20151205_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.SmallIntegerField()),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(to='quiz.Quiz')),
            ],
            options={
                'ordering': ['-payment_date'],
            },
        ),
        migrations.RemoveField(
            model_name='userpayment',
            name='user',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.SmallIntegerField(default=300, verbose_name='Balance($)'),
        ),
        migrations.DeleteModel(
            name='UserPayment',
        ),
        migrations.AddField(
            model_name='quizpayment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
