# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from pinax.eventlog.models import log
from django.conf import settings
from django.utils.html import format_html

from quiz.models import Quiz, QuizAttempt

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password,
                    is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with given email and password
        """
        now = timezone.now()
        if not email:
            raise ValueError('Email is not given')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        return user

    def create_user(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password,
                                False, False, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        s_user = self._create_user(email, username, password,
                                True, True, **extra_fields)
        s_user.is_active = True
        s_user.save()
        return s_user

@python_2_unicode_compatible
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(_('email address'), max_length=255,
                            unique=True, db_index=True)
    balance = models.SmallIntegerField(_('$'), default=0)
    bonus = models.SmallIntegerField(_('Bonus($)'), default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_dayindalushy = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username.lower()[:15]

    def get_absolute_url(self):
        return reverse('update_user')

    def past_quizzes(self):
        count = len(QuizAttempt.objects.filter(student=self).order_by('-date'))
        link = reverse('past_quizzes', args=[self.id])

        return format_html("<a href='{}'>{}</a>", link, count)
    past_quizzes.short_description = 'Quizzes'

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
        log(
            user=self,
            action="USER_SENT_EMAIL",
            extra=
            {
            "to_email":self.email
            }
        )

@python_2_unicode_compatible
class QuizPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    quiz = models.ForeignKey(Quiz)
    amount = models.SmallIntegerField()

    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'payment_%s_%s_%s' % (
            self.user.username,
            self.quiz.name,
            str(self.amount)
        )

@python_2_unicode_compatible
class StarPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    amount = models.SmallIntegerField()
    comment = models.CharField(max_length=80)

    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'starprchs_%s_%s' % (
            self.user.username,
            str(self.amount)
        )