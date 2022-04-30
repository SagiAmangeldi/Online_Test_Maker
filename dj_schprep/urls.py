from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from quiz.views import index as quiz_index
from accounts.views import past_quizzes, quiz_results

urlpatterns = i18n_patterns(
    url(r'^$', quiz_index, name='main_page'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^quiz/', include('quiz.urls', namespace='quiz')),
    url(r'^contact/', include('contact.urls', namespace='contact')),
    url(r'^terms/$', TemplateView.as_view(template_name="terms.html"), name='terms'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^markdown/', include('django_markdown.urls'))
)

urlpatterns += [
    url(regex=r'^baskaru/past_quizzes/user/(?P<user_id>[0-9]+)/$',
        view=past_quizzes,
        name='past_quizzes'
    ),
    url(regex=r'^baskaru/quiz_results/user/(?P<user_id>[0-9]+)/quiz/(?P<quiz_id>[0-9]+)/result/(?P<attempt_id>[0-9]+)/$',
        view=quiz_results,
        name='quiz_results'
    ),
    url(r'^baskaru/', include(admin.site.urls)),
    url(r'^robots.txt$',
        lambda r: HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")
        )

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)