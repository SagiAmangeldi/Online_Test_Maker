from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import contact

urlpatterns = [
    url(regex=r'^contact_us/$',
        view=contact,
        name='contact_us'
    ),
    url(regex=r'contact_us/thanks/$',
        view=TemplateView.as_view(
            template_name='contact/thanks.html'
        ),
        name='thanks'
    )
]
