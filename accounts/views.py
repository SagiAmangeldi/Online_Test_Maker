from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction
from pinax.eventlog.models import log
from django.utils.translation import ugettext as _
from django.http import HttpResponse

from .forms import TransferPointsForm
from .models import CustomUser, QuizPayment, StarPurchase
from quiz.models import Quiz, QuizAttempt, QuestionAttempt


@login_required
def get_balance(request):
    balance = get_user_model().objects.get(
        username=request.user.username
    ).balance
    return HttpResponse("%d" % balance)

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'accounts/update_user.html'
    fields = ['email', 'username']

    def get_object(self, queryset=None):
        return CustomUser.objects.get(
            username=self.request.user.username
        )

@login_required
@transaction.atomic
def transfer_stars(request):
    form = TransferPointsForm(request.POST or None)

    if form.is_valid():
        cd = form.cleaned_data
        amount = int(cd['amount'])

        sender = get_user_model().objects.select_for_update().get(
            username=request.user.username
        )
        recipient = get_user_model().objects.select_for_update().get(
            username=cd['username']
        )
        if sender == recipient:
            return render(
                request,
                'accounts/transfer_stars.html',
                {'form': form,
                "form_error": _("You can't send points to yourself!")}
            )

        if amount > sender.balance:
            return render(
                request,
                'accounts/transfer_stars.html',
                {'form': form,
                "form_error": _("You can't spend more balance than you have!")
                }
            )

        sender.balance -= amount
        sender.save()

        recipient.balance += amount
        recipient.save()

        log(
            user=request.user,
            action="STARS_TRANSFER",
            extra={"amount": amount,
                    "from": sender.username,
                    "to": recipient.username,
                    "sender_balance": sender.balance,
                    "recipient_balance": recipient.balance,
            }
        )
        return HttpResponseRedirect(
            reverse('transfer_stars_done')
        )

    return render(
        request,
        'accounts/transfer_stars.html',
        {'form': form}
    )

@login_required
def payments(request):
    balance = request.user.balance
    log(
        user=request.user,
        action="VIEWED_STAR_SECTION",
        extra={
        "user_balance": balance
        }
    )
    return render(
        request,
        'accounts/star.html'
    )

@login_required
def purchase_stars(request):
    balance = request.user.balance
    log(
        user=request.user,
        action="VIEWED_PURCHASE_STARS_HOWTO",
        extra={
        "user_balance": balance
        }
    )
    return render(
        request,
        'accounts/purchase_stars_howto.html'
    )

@login_required
def quiz_payments(request):
    balance = request.user.balance
    quiz_payments = QuizPayment.objects.filter(
        user=request.user
    ).order_by('-payment_date')

    log(
        user=request.user,
        action="VIEWED_QUIZ_PAYMENTS",
        extra={
        "user_balance": balance
        }
    )

    return render(
        request,
        'accounts/quiz_payments.html',
        {'quiz_payments': quiz_payments}
    )

@login_required
def star_purchases(request):
    balance = request.user.balance
    star_purchases = StarPurchase.objects.filter(
        user=request.user
    ).order_by('-purchase_date')

    log(
        user=request.user,
        action="VIEWED_STAR_PURCHASES",
        extra={
        "user_balance": balance
        }
    )

    return render(
        request,
        'accounts/star_purchases.html',
        {'star_purchases': star_purchases}
    )


from django.contrib import admin
@staff_member_required
def past_quizzes(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    past_attempts = QuizAttempt.objects.filter(student=user).order_by('-date')

    context = admin.site.each_context(request)
    context.update({
        'title': 'Past User Quiz Attempts',
        'past_attempts': past_attempts
    })

    template = 'admin/past_quizzes.html'


    return render(request, template, context)

from django.core.exceptions import ObjectDoesNotExist
@staff_member_required
def quiz_results(request, user_id, quiz_id, attempt_id):

    user = get_object_or_404(CustomUser, pk=user_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    quiz_attempt = get_object_or_404(QuizAttempt, pk=attempt_id, quiz=quiz)

    result_list = []
    questions = quiz.get_questions()

    for q in questions:
        try:
            student_answer = QuestionAttempt.objects.get(
                attempt=quiz_attempt,
                question=q
            ).answer


            result_list.append(
                (q, student_answer)
            )
        except ObjectDoesNotExist:
            continue

    context = admin.site.each_context(request)
    context.update({
        'title': 'Past User Quiz Attempts',
        'user': user,
        'score': quiz_attempt.score(),
        'result_list': result_list
    })
    template = 'admin/quiz_results.html'

    return render(request, template, context)