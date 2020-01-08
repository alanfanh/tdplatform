from django.db import models
from django.contrib.auth.models import User
# Create your models here.


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
    name = models.CharField(verbose_name="组名", max_length=20)
    pl = models.CharField(verbose_name="组长", max_length=10)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """
    用户详细信息表
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    realname = models.CharField(verbose_name="真实姓名", max_length=10)
    email = models.EmailField(verbose_name="邮箱", max_length=32)
    phone = models.CharField(verbose_name="手机号", max_length=11)
    gender = models.CharField(verbose_name="性别", max_length=2)
    group = models.ForeignKey(Group, related_name='group_users', verbose_name="用户所属组", on_delete=models.DO_NOTHING)
    engineer = models.CharField(max_length=10, verbose_name="职位")
    role = models.ForeignKey(Role, related_name='role_users', verbose_name="用户角色", on_delete=models.DO_NOTHING)
    id_card = models.CharField(verbose_name="身份证", max_length=20)
    school = models.CharField(verbose_name="毕业学校", max_length=20)
    gradution_time = models.DateField()
    education = models.CharField(verbose_name="学历", max_length=20)
    pre_job = models.CharField(verbose_name="上一份工作", max_length=20)
    entry_time = models.DateField(verbose_name="入职时间")
    spical_date = models.DateField(verbose_name="生日")
    
    def __str__(self):
        return self.user.username
