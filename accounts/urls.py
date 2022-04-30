from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from registration.backends.hmac.views import RegistrationView, ActivationView
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .views import get_balance
from .views import payments, purchase_stars, transfer_stars, quiz_payments, star_purchases
from .forms import CustomUserRegisterForm

urlpatterns = [
    url(r'^register/$',
        RegistrationView.as_view(
            template_name='accounts/register_init.html',
            email_body_template='accounts/activation_email_body.txt',
            email_subject_template='accounts/activation_email_subj.txt',
            form_class=CustomUserRegisterForm,
        ),
        name='register',
    ),
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='accounts/register_complete.html'
        ),
        name='registration_complete',
    ),
    url(r'^activate/(?P<activation_key>[\w.@+-:]+)/$',
        ActivationView.as_view(),
        name='registration_activate'
    ),
    url(r'^register/activation_complete/$',
        TemplateView.as_view(
            template_name='accounts/register_activation_complete.html'
        ),
        name='registration_activation_complete',
    ),
    url(r'^view/$',
        login_required(
            TemplateView.as_view(
                template_name='accounts/view_user.html'
            )
        ),
        name='view_user',
    ),
    url(r'^login/$',
        auth_views.login,
        name='login',
        kwargs={'template_name': 'accounts/login.html'},
    ),
    url(r'^logout/$',
        auth_views.logout,
        name='logout',
        kwargs={'next_page': reverse_lazy('main_page')}
    ),
    url(r'^password_reset/$',
        auth_views.password_reset,
        name='password_reset',
        kwargs={
            'template_name': 'accounts/password_reset.html',
            'email_template_name': 'accounts/password_reset_email.txt',
            'subject_template_name': 'accounts/password_reset_subject.txt'}
    ),
    url(r'^password_reset/done$',
        auth_views.password_reset_done,
        name='password_reset_done',
        kwargs={'template_name': 'accounts/password_reset_done.html'}
    ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm',
        kwargs={'template_name': 'accounts/password_change_form.html'}
    ),
    url(r'^password_reset/complete$',
        auth_views.password_reset_complete,
        name='password_reset_complete',
        kwargs={'template_name': 'accounts/password_reset_complete.html'}
    ),

    url(r'^payments$',
        payments,
        name='payments',
    ),
    url(r'^payments/purchase_stars$',
        purchase_stars,
        name='purchase_stars',
    ),
    url(r'^payments/transfer_stars$',
        transfer_stars,
        name='transfer_stars',
    ),
    url(r'^payments/transfer_stars/done$',
        TemplateView.as_view(
            template_name='accounts/transfer_stars_done.html'
        ),
        name='transfer_stars_done',
    ),
    url(r'^payments/get_balance$',
        get_balance,
        name='get_balance',
    ),
    url(r'^payments/star_purchases$',
        star_purchases,
        name='star_purchases',
    ),
    url(r'^payments/quiz_payments$',
        quiz_payments,
        name='quiz_payments',
    )
]