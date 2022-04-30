from django.contrib.auth.signals import user_logged_in, user_logged_out
from registration.signals import user_registered, user_activated
from django.dispatch import receiver
from django.conf import settings
from pinax.eventlog.models import log

from django.contrib.auth import login

@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    log(
        user=request.user,
        action="LOGGED_IN",
        extra={"IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')}
    )

@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    log(
        user=request.user,
        action="LOGGED_OUT",
        extra={"IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')}
    )

@receiver(user_registered)
def sig_user_registered(sender, user, request, **kwargs):
    log(
        user=user,
        action="REGISTERED",
        extra={"IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')}
    )

@receiver(user_activated)
def sig_user_activated(sender, user, request, **kwargs):
    log(
        user=user,
        action="ACTIVATED",
        extra={"IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')}
    )

    login(request, user)