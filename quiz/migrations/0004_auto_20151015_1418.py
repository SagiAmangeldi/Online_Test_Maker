# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0003_quizpurchase_is_quiz_permitted'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_permitted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='quizpurchase',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='description',
        ),
        migrations.RemoveField(
            model_name='quizpurchase',
            name='is_quiz_permitted',
        ),
        migrations.AlterField(
            model_name='quizattempt',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='quizpurchase',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='quizpermission',
            name='quiz',
            field=models.ForeignKey(to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='quizpermission',
            name='student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
