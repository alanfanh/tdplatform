from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify

class ArticleColumn(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING ,related_name="article_column")
    column = models.CharField(verbose_name="栏目", max_length=50)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column

class ArticlePost(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING, related_name="author_article")
    title = models.CharField(verbose_name="标题", max_length=100)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, verbose_name="栏目", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now(), auto_now=False, auto_now_add=False)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id,self.slug])
    
