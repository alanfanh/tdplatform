from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from account.models import Group

class BlogArticles(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title
