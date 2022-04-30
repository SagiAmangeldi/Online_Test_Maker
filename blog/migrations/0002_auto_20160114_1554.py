# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='figure',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=155),
        ),
    ]
