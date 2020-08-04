from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=128, db_index=True, null=True)
    draft = models.BooleanField(default=True)

    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Reply(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.content
