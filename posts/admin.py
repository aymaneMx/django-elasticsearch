from django.contrib import admin

from posts.models import Post, Reply

admin.site.register(Post)
admin.site.register(Reply)
