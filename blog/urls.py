from django.conf.urls import url
from .views import all_posts, single_post

urlpatterns = [
    url(regex=r'^$',
        view=all_posts,
        name='posts'
    ),
    url(regex=r'^post/(?P<slug>[-\w]+)/$',
        view=single_post,
        name='post'
    )
]