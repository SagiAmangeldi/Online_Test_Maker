from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.db import transaction

from .forms import take_quiz_form
from .models import Subject, Answer, QuestionAttempt
from .models import Quiz, QuizAttempt, QuizPurchase, QuizPermission

from blog.models import Post
from accounts.models import QuizPayment
from django.views.decorators.cache import never_cache
from pinax.eventlog.models import log

def index(request):

    posts = Post.objects.filter(publish=True)

    if request.user.is_authenticated():
        log(
            user=request.user,
            action="VIEWED_HOME_PAGE",
            extra={"IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')}
        )

        student = request.user
        past_attempts = QuizAttempt.objects.filter(
            student=student
        ).order_by('-date')
        balance = student.balance
        
        #Number of (unique) quizzes user took in each Subject
        subject_data = []
        for subject in Subject.objects.filter(is_active=True).order_by('list_order'):
            total = len(Quiz.objects.filter(subject=subject, is_active=True))
            taken = len(set(map(lambda x: x.quiz.id, QuizAttempt.objects.filter(student=student, quiz__subject=subject))))
            percent = 0 if taken == 0 else int(round(taken*100)/round(total))
            subject_data.append(
                {
                    'subject':subject,
                    'total': total,
                    'taken': taken,
                    'percent':percent
                 }
            )

        return render(
            request, 
            'loggedin_main.html',
            {
                "past_attempts": past_attempts, 
                "balance":balance, 
                "posts": posts,
                "subject_data": subject_data
            }
        )

    return render(request, "public_main.html", {"posts": posts})

@login_required
def list_subj_quizzes(request, subj_id):
    subj = get_object_or_404(Subject, pk=subj_id)
    quizzes = Quiz.objects.filter(is_active=True, subject=subj)
    balance = request.user.balance

    passed_quiz_ids = []
    for qa in QuizAttempt.objects.filter(
        student=request.user
    ):
        if qa.quiz.pk not in passed_quiz_ids and qa.quiz in quizzes:
            passed_quiz_ids.append(qa.quiz.pk)

    qperms = QuizPermission.objects.filter(
        student=request.user
    ).filter(is_permitted=True)

    permitted_quiz_ids = [x.quiz.pk for x in qperms]

    log(
        user=request.user,
        action="VIEWED_QUIZ_LIST_%s" % subj,
        extra=
        {
        "user_balance": balance,
        "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
        }
    )

    return render(
        request,
        'quiz/list_subj_quizzes.html',
        {
        'quizzes': quizzes,
        'passed_quiz_ids': passed_quiz_ids,
        'permitted_quiz_ids': permitted_quiz_ids,
        'subject': subj.name,
        }
    )

@login_required
@never_cache
def checkout_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if not quiz.is_active and request.user.username not in ('admin', 'teacher'):
        log(
            user=request.user,
            action="PERMISSION_DENIED",
            obj=quiz,
            extra=
            {
            "view": "checkout_quiz",
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )
        raise PermissionDenied

    balance = request.user.balance
    request.session['warned_%d' % quiz.pk] = 'Yes'

    log(
        user=request.user,
        action="CHECKED_OUT_QUIZ",
        obj=quiz,
        extra={"user_balance": balance, "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')}
    )
    return render(
        request,
        "quiz/checkout_quiz.html",
        {
        'quiz': quiz,
        'balance':balance
        }
    )

@login_required
@transaction.atomic
@never_cache
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(
        Quiz,
        pk=quiz_id
    )
    student = get_user_model().objects.select_for_update().get(
        username=request.user.username
    )
    balance = student.balance

    is_hidden_allowed = quiz.is_active or student.username in ('admin', 'teacher')

    if not is_hidden_allowed:
        log(
            user=request.user,
            action="PERMISSION_DENIED",
            obj=quiz,
            extra={
            "view": "take_quiz",
            "user_balance": balance,
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )
        raise PermissionDenied

    quiz_form = take_quiz_form(quiz)
    if request.method == "POST":
        form = quiz_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            quiz_attempt = QuizAttempt.objects.create(
                student = request.user,
                quiz = quiz
            )

            for k in cd.keys():
                answer = get_object_or_404(
                    Answer, pk=cd[k]
                )
                question = answer.question
                attempt = QuestionAttempt(
                    attempt = quiz_attempt,
                    question = question,
                    answer = answer
                )
                attempt.save()

            if quiz.price != 0:
                qperm = QuizPermission.objects.get(
                    quiz=quiz,
                    student=student
                )
                qperm.is_permitted = False
                qperm.save()

            if ('warned_%d' % quiz.pk) in request.session:
                del request.session['warned_%d' % quiz.pk]
            log(
                user=request.user,
                action="SUBMITTED_QUIZ",
                obj=quiz,
                extra={"user_balance": balance, "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')}
            )
            return HttpResponseRedirect(
                reverse(
                    'quiz:quiz_result',
                    args=(
                        quiz_id,
                        quiz_attempt.pk
                    )
                )
            )
        else:
            log(
                user=request.user,
                action="SUBMITTED_INVALID_QUIZ",
                obj=quiz,
                extra={"user_balance": balance}
            )
            return render(request,
                'quiz/take_quiz.html',
                {
                'form': form,
                'quiz': quiz,
                'form_error': _('Error: please answer all of the quizzes.')
                }
            )
    else:
        qperm = QuizPermission.objects.filter(
            quiz=quiz,
            student=student
        )

        is_permitted = False
        if qperm.exists():
            is_permitted = qperm[0].is_permitted

        if is_permitted or quiz.price == 0:
            log(
                user=request.user,
                action="TOOK_QUIZ",
                obj=quiz,
                extra={
                "user_balance": balance,
                "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
                }
            )
            return render(
                request,
                'quiz/take_quiz.html',
                {
                'form': quiz_form,
                'quiz': quiz,
                'quiz_price': quiz.price
                }
            )

        is_warned = request.session.get('warned_%d' % quiz.pk, 'No') == 'Yes'
        if not is_warned:
            log(
                user=request.user,
                action="REDIRECTED_TO_CHECKOUT",
                obj=quiz,
                extra={
                "view": "take_quiz",
                "user_balance": balance,
                "quiz_price": quiz.price,
                "q_perm": is_permitted
                }
            )
            return HttpResponseRedirect(
                reverse(
                    'quiz:checkout_quiz', args=(quiz.pk,)
                )
            )

        if quiz.price > balance:
            log(
                user=request.user,
                action="PERMISSION_DENIED",
                obj=quiz,
                extra={
                "view": "take_quiz",
                "user_balance": balance,
                "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
                }
            )
            raise PermissionDenied

        qpurchase = QuizPurchase(
            quiz=quiz,
            student=student,
            price=quiz.price
        )
        qpurchase.save()
        student.balance -= quiz.price
        student.save()

        QuizPayment.objects.create(
            user = student,
            amount = quiz.price,
            quiz = quiz
        )

        log(
            user=request.user,
            action="MONEY_DEDUCTED",
            obj=quiz,
            extra={
            "user_balance": balance,
            "amount (quiz_price)":quiz.price,
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )

        deduction_info = '%d pts has been deducted from your balance.' % quiz.price


        qperm = QuizPermission.objects.filter(
            quiz=quiz,
            student=student
        )
        if not qperm.exists():
            QuizPermission.objects.create(
                quiz=quiz,
                student=student,
                is_permitted=True
            )

        perm = QuizPermission.objects.select_for_update().get(
            student=request.user,
            quiz=quiz
        )
        perm.is_permitted = True
        perm.save()

        log(
            user=request.user,
            action="TOOK_QUIZ",
            obj=quiz,
            extra={
            "user_balance": balance,
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )
        return render(
            request,
            'quiz/take_quiz.html',
            {
            'form': quiz_form,
            'quiz': quiz,
            'deduct_info': deduction_info,
            'quiz_price': quiz.price
            }
        )

def take_free_quiz(request, quiz_id):
    quiz = get_object_or_404(
        Quiz,
        pk=quiz_id,
        price=0,
        is_active=True
    )

    quiz_form = take_quiz_form(quiz)

    return render(
        request,
        'quiz/take_free_quiz.html',
        {
            'form': quiz_form,
            'quiz': quiz
        }
    )

def free_quiz_result(request, quiz_id):
    quiz = get_object_or_404(
        Quiz,
        pk=quiz_id,
        price=0,
        is_active=True
    )

    quiz_form = take_quiz_form(quiz)
    if request.method == "POST":
        form = quiz_form(request.POST)
        
        if form.is_valid():
            result_list = []
            
            cd = form.cleaned_data
            score = 0
            for k in cd.keys():
                answer = get_object_or_404(
                    Answer, pk=cd[k]
                )
                if answer.is_correct:
                    score += 1
                question = answer.question
                result_list.append(
                    (question, answer)
                )
            
            return render(
                request,
                "quiz/quiz_results.html",
                {
                    "quiz": quiz,
                    "score": score,
                    "result_list": result_list,
                    "is_public_test": True
                }
            )

        else:
            log(
                user=request.user,
                action="SUBMITTED_INVALID_QUIZ(FREE QUIZ)",
                obj=quiz,
            )
            return render(request,
                'quiz/take_free_quiz.html',
                {
                    'form': form,
                    'quiz': quiz,
                    'form_error': _('Error: please answer all of the quizzes.')
                }
            )

    else:
        return HttpResponseRedirect(
                reverse(
                    'quiz:take_free_quiz', args=(quiz.pk,)
                )
            )

@login_required
@never_cache
def quiz_result(request, quiz_id, attempt_id):
    quiz = get_object_or_404(
        Quiz,
        pk=quiz_id
    )
    quiz_attempt = get_object_or_404(
        QuizAttempt,
        pk = attempt_id,
        quiz=quiz
    )

    student = request.user
    balance = student.balance

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

    log(
        user=request.user,
        action="VIEWED_QUIZ_RESULT",
        obj=quiz,
        extra={
            "user_balance": balance,
            "problem_cnt": quiz.question_count,
            "score": quiz_attempt.score(),
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
        }
    )
    if request.user == quiz_attempt.student:
        return render(
            request,
            "quiz/quiz_results.html",
            {
            "quiz": quiz,
            "score": quiz_attempt.score(),
            "result_list": result_list,
            }
        )
    else:
        log(
            user=request.user,
            action="PERMISSION_DENIED",
            obj=quiz,
            extra={
            "view": "quiz_result",
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )
        raise PermissionDenied

@login_required
def quiz_solution(request, quiz_id):
    quiz = get_object_or_404(
        Quiz,
        pk=quiz_id
    )
    questions = quiz.get_questions()

    student = request.user
    balance = student.balance

    qp = QuizAttempt.objects.filter(
        student=request.user,
        quiz=quiz
    )
    if not qp:
        log(
            user=request.user,
            action="PERMISSION_DENIED",
            obj=quiz,
            extra={
            "view": "quiz_solution",
            "reason": "not his own solutions",
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )
        raise PermissionDenied

    log(
        user=request.user,
        action="VIEWED_QUIZ_SOLUTION",
        obj=quiz,
        extra={
        "user_balance": balance,
        "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
        }
    )
    return render(
        request,
        'quiz/quiz_solution.html',
        {
        'quiz': quiz,
        'questions': questions
        }
    )

@login_required
def progress_history(request):
    student = request.user
    past_attempts = QuizAttempt.objects.filter(
        student=student
    ).order_by('-date')
    balance = student.balance

    log(
        user=request.user,
        action="VIEWED_PROGRESS_HISTORY",
        extra={
        "user_balance": balance,
        "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
        }
    )
    return render(
        request,
        "quiz/progress_history.html",
        {
        "past_attempts": past_attempts,
        "user_balance": balance
        }
    )