from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    """
    用户详细信息表
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    realname = models.CharField(max_length=10)
    email = models.EmailField(max_length=32)
    phone = models.CharField(max_length=11)
    gender = models.CharField(max_length=2)
    group = models.ForeignKey("Group", verbose_name="用户所属组", on_delete=models.CASCADE)
    engineer = models.CharField(max_length=10, verbose_name="职位")
    role = models.ForeignKey("Role", verbose_name="用户角色", on_delete=models.CASCADE)
    id_card = models.CharField(max_length=20)
    school = models.CharField(max_length=20)
    gradution_time = models.DateField()
    education = models.CharField(max_length=20)
    pre_job = models.CharField(max_length=20)
    entry_time = models.DateField()
    spical_date = models.DateField()
    
    def __str__(self):
        return self.user.username


class Role(models.Model):
    """
    用户角色表
    """
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.role_name
    

class Group(models.Model):
    """
    部门组信息
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    pl = models.CharField(max_length=10)

    def __str__(self):
        return self.name