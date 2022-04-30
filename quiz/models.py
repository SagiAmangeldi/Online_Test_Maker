# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import json

from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

@python_2_unicode_compatible
class Subject(models.Model):

    name = models.CharField(
        max_length=250,
        blank=True,
        unique=True,
        null=True
    )

    list_order = models.PositiveSmallIntegerField(
        verbose_name=_("List Order"),
        help_text=_("Desired order in the list; ascending (i.e. 0 = topmost)"),
        default=0
    )

    is_active = models.BooleanField(
        blank=False,
        null=False,
        default=False
    )

    icon = models.FileField(
        upload_to='uploads/subject_icons/',
        blank=True,
        null=True,
        help_text=_("Subject icon to be displayed along with Subject name")
    )

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Quiz(models.Model):

    name = models.CharField(
        max_length=60,
        blank=False
    )

    is_active = models.BooleanField(
        blank=False,
        null=False,
        default=False,
    )

    subject = models.ForeignKey(
        Subject,
        null=True,
        blank=True,
        verbose_name=_("Subject")
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    price = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name=_("Price"),
        default=0
    )

    duration = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name=_("Duration"),
        default=0
    )

    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()

    @property
    def question_count(self):
        return self.get_questions().count()

    class Meta:
        verbose_name = _("Quiz/Test")
        verbose_name_plural = _("Quizzes/Tests")
        ordering = ['subject', 'name']

@python_2_unicode_compatible
class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """

    quiz = models.ForeignKey(Quiz, blank=True)

    figure = models.ImageField(
        upload_to='uploads/question/%Y-%m-%d/',
        blank=True,
        null=True,
        help_text=_("Image to go with problem statement")
    )

    content = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        help_text=_("Question text")
    )

    solution = models.TextField(
        max_length=2000,
        blank=True,
        help_text=_("Solution content")
    )

    solutionfigure = models.ImageField(
        upload_to='uploads/question/%Y-%m-%d/',
        blank=True,
        null=True,
        help_text=_("Solution in the form of image")
    )

    def __str__(self):
        return 'question_%d' % self.id

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def get_correct_answer(self):
        cor_ans = Answer.objects.filter(question=self).filter(is_correct=True)
        if cor_ans:
            return cor_ans[0]
        else:
            return None

@python_2_unicode_compatible
class Answer(models.Model):
    question = models.ForeignKey(Question)

    content = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=_("Answer content")
    )

    figure = models.ImageField(
        upload_to='uploads/answer/%Y-%m-%d/',
        null=True,
        blank=True
    )

    is_correct = models.BooleanField(
        blank=False,
        default=False,
        help_text=_("Is this the correct answer?")
    )

    def __str__(self):
        return 'answer_%d' % self.id

@python_2_unicode_compatible
class QuizAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL
    )
    quiz = models.ForeignKey(Quiz)
    date = models.DateTimeField(
        auto_now_add=True
    )

    def score(self):
        total = 0
        for question in self.questionattempt_set.all():
            if question.answer.is_correct:
                total += 1
        return total

    def __str__(self):
        return '%s-%d-%s' % (
            self.student.username,
            self.quiz.id,
            str(self.date)
        )

@python_2_unicode_compatible
class QuestionAttempt(models.Model):
    attempt = models.ForeignKey(QuizAttempt)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    attemptdate = models.DateTimeField(
        auto_now_add=True
    )

    def is_correct(self):
        return self.answer.is_correct()

    def __str__(self):
        return '%d_%s' % (
            self.question.id,
            self.attempt
        )

@python_2_unicode_compatible
class QuizPurchase(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL)
    quiz = models.ForeignKey(Quiz)
    date = models.DateTimeField(auto_now_add=True)
    price = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '%s_%s' % (
            self.student.username,
            self.quiz.name
        )

@python_2_unicode_compatible
class QuizPermission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL)
    quiz = models.ForeignKey(Quiz)
    is_permitted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Perm_%s_%s' % (
            self.student.username,
            self.quiz.name
        )

@python_2_unicode_compatible
class Package(models.Model):
    quizzes = models.ManyToManyField(Quiz)

    name = models.CharField(
        max_length=60,
        blank=False
    )

    is_active = models.BooleanField(
        blank=False,
        null=False,
        default=False
    )

    price = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name=_("Price"),
        default=0
    )

    listing_order = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name=_("Listing Order"),
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Quiz Package")
        verbose_name_plural = _("Quiz Packages")
        ordering = ['listing_order']

@python_2_unicode_compatible
class PackagePurchase(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL)
    package = models.ForeignKey(Package)
    date = models.DateTimeField(auto_now_add=True)
    price = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '%s_%s' % (
            self.student.username,
            self.package.name
        )