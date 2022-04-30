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
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(help_text='Answer content', max_length=1000, null=True, blank=True)),
                ('figure', models.ImageField(null=True, upload_to='uploads/answer/%Y-%m-%d/', blank=True)),
                ('is_correct', models.BooleanField(default=False, help_text='Is this the correct answer?')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('figure', models.ImageField(help_text='Image to go with problem statement', null=True, upload_to='uploads/question/%Y-%m-%d/', blank=True)),
                ('content', models.CharField(help_text='Question text', max_length=1000, null=True, blank=True)),
                ('solution', models.TextField(help_text='Solution content', max_length=2000, blank=True)),
                ('solutionfigure', models.ImageField(help_text='Solution in the form of image', null=True, upload_to='uploads/question/%Y-%m-%d/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='quiz.Answer', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.PositiveSmallIntegerField(default=0, help_text='Price of Quiz (0 if free)', verbose_name='Price')),
                ('duration', models.PositiveSmallIntegerField(default=0, help_text='Duration of Quiz in minutes (0 if unlimited)', verbose_name='Duration')),
            ],
            options={
                'verbose_name': 'Quiz/Test',
                'verbose_name_plural': 'Quizzes/Tests',
            },
        ),
        migrations.CreateModel(
            name='QuizAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('quiz', models.ForeignKey(to='quiz.Quiz')),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('price', models.SmallIntegerField(default=0)),
                ('quiz', models.ForeignKey(to='quiz.Quiz')),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, unique=True, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(verbose_name='Subject', blank=True, to='quiz.Subject', null=True),
        ),
        migrations.AddField(
            model_name='questionattempt',
            name='attempt',
            field=models.ForeignKey(to='quiz.QuizAttempt'),
        ),
        migrations.AddField(
            model_name='questionattempt',
            name='question',
            field=models.ForeignKey(to='quiz.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(to='quiz.Quiz', blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='quiz.Question'),
        ),
    ]
