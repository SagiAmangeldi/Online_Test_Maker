# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publish', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=65)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=155)),
                ('content', models.TextField()),
                ('figure', models.ImageField(null=True, upload_to=b'uploads/blog/%Y-%m-%d/', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
    ]
