from django.conf.urls import url
from .views import list_subj_quizzes, progress_history
from .views import checkout_quiz, take_quiz, quiz_result, quiz_solution
from .views import take_free_quiz, free_quiz_result

urlpatterns = [
    url(regex=r'^list_quizzes/(?P<subj_id>[0-9]+)/$',
        view=list_subj_quizzes,
        name='list_subj_quizzes'
    ),
    url(regex=r'^(?P<quiz_id>[0-9]+)/$',
        view=checkout_quiz,
        name='checkout_quiz'
    ),
    url(regex=r'^take/(?P<quiz_id>[0-9]+)/$',
        view=take_quiz,
        name='take_quiz'
    ),
    url(regex=r'^(?P<quiz_id>[0-9]+)/result/(?P<attempt_id>[0-9]+)/$',
        view=quiz_result,
        name='quiz_result'
    ),
    url(regex=r'^(?P<quiz_id>[0-9]+)/solution/$',
        view=quiz_solution,
        name='quiz_solution'
    ),
    url(regex=r'^progress_history/$',
        view=progress_history,
        name='progress_history'
    ),
    url(regex=r'^take_free_quiz/(?P<quiz_id>[0-9]+)/$',
        view=take_free_quiz,
        name='take_free_quiz'
    ),
    url(regex=r'^free_quiz_result/(?P<quiz_id>[0-9]+)/$',
        view=free_quiz_result,
        name='free_quiz_result'
    )
]