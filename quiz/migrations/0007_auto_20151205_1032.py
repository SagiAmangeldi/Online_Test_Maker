# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20151129_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['subject', 'name'], 'verbose_name': '\u0422\u0435\u0441\u0442', 'verbose_name_plural': '\u0422\u0435\u0441\u0442\u0442\u0435\u0440'},
        ),
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=models.CharField(help_text='\u0416\u0430\u0443\u0430\u043f \u043c\u04d9\u0442\u0456\u043d\u0456', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, help_text='\u041e\u0441\u044b \u0434\u04b1\u0440\u044b\u0441 \u0436\u0430\u0443\u0430\u043f \u043f\u0430?'),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(help_text='\u0421\u04b1\u0440\u0430\u049b \u043c\u04d9\u0442\u0456\u043d\u0456', max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='figure',
            field=models.ImageField(help_text='\u0421\u04b1\u0440\u0430\u049b\u0442\u044b\u043d \u0441\u0443\u0440\u0435\u0442\u0456', null=True, upload_to='uploads/question/%Y-%m-%d/', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='solution',
            field=models.TextField(help_text='\u0428\u0435\u0448\u0456\u043c \u043c\u04d9\u0442\u0456\u043d\u0456', max_length=2000, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='solutionfigure',
            field=models.ImageField(help_text='\u0428\u0435\u0448\u0456\u043c \u0441\u0443\u0440\u0435\u0442\u0456', null=True, upload_to='uploads/question/%Y-%m-%d/', blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, help_text='\u0422\u0435\u0441\u0442 \u0431\u0430\u0493\u0430\u0441\u044b (0 \u0431\u043e\u043b\u0441\u0430 \u0442\u0435\u0433\u0456\u043d)', verbose_name='\u0411\u0430\u0493\u0430\u0441\u044b'),
        ),
    ]
