from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from .models import Post, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1

class PostAdmin(MarkdownModelAdmin):
    model = Post

    prepopulated_fields = {'slug': ('title',)}
    list_display = ("title", "creation_date")
    inlines = (PostImageInline, )

admin.site.register(Post, PostAdmin)
