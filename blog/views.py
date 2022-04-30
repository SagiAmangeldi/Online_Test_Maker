from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pinax.eventlog.models import log
from .models import Post

def all_posts(request):
    post_list = Post.objects.filter(publish=True)
    paginator = Paginator(post_list, 13)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    try:
        log(
            user=request.user,
            action="VIEWED_NEWS_LIST",
            extra=
            {
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )
    except:
        log(
            user=request.user,
            action="VIEWED_NEWS_LIST",
            extra=
            {
            "-": "exception happened but user saw the news"
            }
        )

    return render(
        request,
        'blog/all.html',
        {'posts': posts}
    )

def single_post(request, slug):
    post = get_object_or_404(Post, slug=slug, publish=True)

    try:
        log(
            user=request.user,
            action="VIEWED_NEWS",
            extra=
            {
            "slug": post.slug,
            "IP": request.META.get('HTTP_X_REAL_IP', 'NO_IP')
            }
        )
    except:
        log(
            user=request.user,
            action="VIEWED_NEWS",
            extra=
            {
            "-": "exception happened but user saw the news"
            }
        )

    return render(
        request,
        'blog/single.html',
        {'post': post}
    )
