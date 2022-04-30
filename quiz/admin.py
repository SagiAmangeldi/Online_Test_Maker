# -*-encoding: utf-8 -*-
from django.contrib import admin
from django.forms import ModelForm
from django.forms import ModelForm, Select, TextInput, NumberInput
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
from .models import Quiz, Subject, Question, Answer, QuizPurchase, QuizPermission, QuizAttempt

from suit import apps

from suit.admin import RelatedFieldAdmin, get_related_field
from suit.admin_filters import IsNullFieldListFilter
from suit.sortables import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import AutosizedTextarea, EnclosedInput

class ColorInput(TextInput):
    input_type = 'color'

class AnswerSuperInline(SuperInlineModelAdmin, admin.TabularInline):
    model = Answer
    extra = 4

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra

class QuestionInlineForm(ModelForm):
    class Meta:
        widgets = {
            'content': AutosizedTextarea(attrs={'rows': 3}),
            'solution': AutosizedTextarea(attrs={'rows': 3})
        }

class QuestionInline(SuperInlineModelAdmin, admin.StackedInline):
    form = QuestionInlineForm
    model = Question
    inlines = (AnswerSuperInline, )
    extra = 1

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra

def activate_quiz(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_quiz.short_description = "Activate selected quizzes"

def deactivate_quiz(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_quiz.short_description = "Deactivate selected quizzes"

class QuizAdminForm(ModelForm):
    class Meta:
        widgets = {
            'html5_color': ColorInput,
            'html5_number': NumberInput,
            'textfield': AutosizedTextarea(attrs={'rows': 3})
        }

@admin.register(Quiz)
class QuizAdmin(SuperModelAdmin):
    def problems(self, quiz):
        return len(Question.objects.filter(quiz=quiz))

    form = QuizAdminForm
    fields = (('subject', 'is_active'), 'name', 'price',)
    list_display = ('name', 'is_active', 'subject', 'price', 'problems' )
    list_filter = ('subject',)

    inlines = (QuestionInline, )

    actions = [activate_quiz, deactivate_quiz]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name',
                           'icon',
                           ('is_active', 'list_order')],
                'classes': ('suit-tab suit-tab-general',),
                }
         )
    ]

    suit_form_size = {
            'fields': {
                'name': apps.SUIT_FORM_SIZE_SMALL,
                'list_order': apps.SUIT_FORM_SIZE_SMALL,
            }
    }

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#
#     list_display = ('quiz', 'content')
#     list_filter = ('quiz', )
#     fields = ('quiz', 'content', 'figure', 'solution', 'solutionfigure')
#
#     search_fields = ('content', )
#
#     inlines = [AnswerInline]

@admin.register(QuizPurchase)
class QuizPurchaseAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'student', 'price', 'date')

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def get_actions(self, request):
        actions = []
        return actions
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(QuizPermission)
class QuizPermissionAdmin(admin.ModelAdmin):
    list_display = ('created', 'quiz', 'student', 'is_permitted')
    list_filter = ('student', 'is_permitted')

class LogAdmin(admin.ModelAdmin):
    def quiz_name(obj):
        quiz = Quiz.objects.filter(pk=obj.object_id)
        if quiz.exists():
            return "%s" % (quiz[0].name)
        else:
            return 'None'
    quiz_name.short_description = 'Quiz_Name'

    raw_id_fields = ["user"]
    list_filter = ["action", "timestamp"]
    list_display = ["timestamp", "user", "action", "extra", "object_id", quiz_name]
    search_fields = ["user__username", "user__email", "extra"]

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def get_actions(self, request):
        actions = []
        return actions
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.site_header = 'Dayindal Command & Control Center'
admin.site.site_title = 'Dayindal Admin'
#admin.site.unregister(Log)
#admin.site.register(Log, LogAdmin)