# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.db import transaction
from django.contrib import messages

from django.core.mail import send_mail
from email.mime.text import MIMEText

from pinax.eventlog.models import log
from .models import CustomUser, QuizPayment, StarPurchase
import datetime


class UpdateActionForm(ActionForm):
    points = forms.IntegerField(required=False)
    comment = forms.CharField(required=False)

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {'fields': ('username', 'email', 'balance', 'password')}
        ),
        (
            _('Permissions'),
            {
            'fields':(('is_active', 'is_staff', 'is_dayindalushy'), 'user_permissions'),
            'classes': ('collapse',),
            }
        ),
    )

    def activate_user(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Successfully activated %d user(s).") % queryset.count() )
    activate_user.short_description = _("Activate selected users")

    def deactivate_user(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Successfully deactivated %d user(s).") % queryset.count() )
    deactivate_user.short_description = _("Deactivate selected users")

    @transaction.atomic
    def add_points(self, request, queryset):
        if request.POST['points']:
            points = request.POST['points']
            comment = request.POST['comment']

            points = int(points)
            if points > 0:
                for q in queryset:
                    q.balance += points
                    q.save()

                    StarPurchase.objects.create(
                        user = q,
                        amount = points,
                        comment = comment
                    )

                    # Send Email
                    date_str = datetime.date.today().strftime("%d/%m/%Y")
                    em_subj = "[{date}] Төлем / Оплата".format(date=date_str)
                    
                    em_cont = u"""Құрметті {username}, www.dayindal.com сайтындағы аккаунтыңызға {amount} стар салынды.\n\n------\n\nУважаемый (ая) {username}, на ваш аккаунт на сайте www.dayindal.com поступило {amount} стар.""".format(username=q.username, amount=points)

                    send_mail(
                        em_subj,
                        em_cont,
                        'Dayindal Support <support@dayindal.com>',
                        [q.email],
                    )

                    log(user=q,
                        action="ADMIN_ADDED_POINTS",
                        extra={"amount": points}
                    )

                self.message_user(request, "Successfully added %d points to %d user(s)." % (points, queryset.count()) )
            else:
                messages.error(request, "Negative points not allowed")
    add_points.short_description = _('Add points to selected users')

    @transaction.atomic
    def remove_points(self, request, queryset):
        if request.POST['points']:
            points = request.POST['points']
            points = int(points)
            couldnt_remove = 0
            if points > 0:
                for q in queryset:
                    if q.balance >= points:
                        q.balance -= points
                        q.save()
                        log(user=q,
                            action="ADMIN_REMOVED_POINTS",
                            extra={"amount": points}
                        )
                    else:
                        messages.error(request, "One of users has less balance than you're trying to deduct.")
                        couldnt_remove += 1
                self.message_user(request, "Successfully removed %d points from %d user(s)." % (points, queryset.count() - couldnt_remove) )
            else:
                messages.error(request, "Negative points not allowed")

    remove_points.short_description = _('Remove points from selected users')


    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('username',)
        return self.readonly_fields

    list_display = ('email', 'username', 'is_active', 'is_staff',
                    'past_quizzes', 'balance', 'date_joined', 'last_login')
    readonly_fields = ('last_login', 'date_joined', 'balance', 'past_quizzes')
    search_fields = ('email', 'username')
    order = ('-date_joined', )

    actions = [activate_user, deactivate_user, add_points, remove_points]
    action_form = UpdateActionForm

admin.site.register(CustomUser, CustomUserAdmin)

class QuizPaymentAdmin(admin.ModelAdmin):

    list_display = ('id', 'user','quiz', 'amount', 'payment_date')
    list_filter = ('user', 'quiz')
    # fields = ('user','quiz', 'amount', 'payment_date')
    # readonly_fields = ('user','quiz', 'amount', 'payment_date')

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def get_actions(self, request):
        #Disable delete
        actions = []
        return actions
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

admin.site.register(QuizPayment, QuizPaymentAdmin)

class StarPurchaseAdmin(admin.ModelAdmin):

    list_display = ('user','amount', 'purchase_date', 'comment')
    search_fields = ('user', )
    #fields = ('user','amount', 'comment', 'purchase_date')
    #readonly_fields = ('purchase_date',)

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def get_actions(self, request):
        #Disable delete
        actions = []
        return actions
    def has_delete_permission(self, request, obj=None):
        #Disable delete
        return False

admin.site.register(StarPurchase, StarPurchaseAdmin)

from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.flatpages.models import FlatPage
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(FlatPage)