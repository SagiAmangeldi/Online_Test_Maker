from django import forms
from django.forms.widgets import RadioSelect, Textarea

# class QuizForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         #.. do sth here
#         super(QuizForm, self).__init__(*args, **kwargs)

def take_quiz_form(quiz):
    """takes a quiz object and returns a form
    with all questions associated with the it"""

    fields = {}
    questions = quiz.question_set.all()
    for q in questions:
        field_name = "question_%d" % q.pk
        choice_list = []
        for answer in q.answer_set.all():
            choice_list.append((answer.pk, answer.content))
        fields[field_name] = forms.ChoiceField(label=q.content,
                                               required=True,
                                               choices=choice_list,
                                               widget=forms.RadioSelect)

    return type('TakeQuizForm', (forms.BaseForm,), {'base_fields': fields})
