# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20151024_1912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['subject', 'name'], 'verbose_name': 'Quiz/Test', 'verbose_name_plural': 'Quizzes/Tests'},
        ),
        migrations.AlterField(
            model_name='quiz',
            name='price',
            field=models.PositiveSmallIntegerField(default=0, help_text='Price of Quiz (0 if free)', verbose_name='\u0411\u0430\u0493\u0430\u0441\u044b'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(verbose_name='\u041f\u04d9\u043d', blank=True, to='quiz.Subject', null=True),
        ),
    ]
