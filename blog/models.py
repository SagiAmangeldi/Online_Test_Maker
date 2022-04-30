from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django_markdown.models import MarkdownField

class Post(models.Model):
    publish = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=155)
    content = MarkdownField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_date',]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[str(self.slug)])

class PostImage(models.Model):
    post = models.ForeignKey(Post)
    image = models.ImageField(
        upload_to='uploads/blog_img/%Y-%m-%d/',
        blank=True,
        null=True,
        help_text="Image to go with blog posts"
    )
