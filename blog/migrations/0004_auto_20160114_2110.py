# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160114_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AddField(
            model_name='postimage',
            name='post',
            field=models.ForeignKey(default=1, to='blog.Post'),
            preserve_default=False,
        ),
    ]
