from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class ArticleColumn(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    column = models.CharField(verbose_name="栏目", max_length=50)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


