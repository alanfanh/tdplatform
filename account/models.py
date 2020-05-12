from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Role(models.Model):
    """
    用户角色表
    """
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=10)

    class Meta:
        verbose_name = "用户角色"
        verbose_name_plural = "用户角色"

    def __str__(self):
        return self.role_name


class Group(models.Model):
    """
    部门组信息
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="组名", max_length=20)
    pl = models.CharField(verbose_name="组长", max_length=10)

    class Meta:
        verbose_name = "用户小组"
        verbose_name_plural = "用户小组"

    def __str__(self):
        return self.name

class Rank(models.Model):
    """
    员工职级
    """
    id = models.AutoField(primary_key=True)
    rank_name = models.CharField(verbose_name="职级",max_length=5)

    def __str__(self):
        return self.rank_name
    

class UserInfo(models.Model):
    """
    用户详细信息表
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    job_num = models.CharField(verbose_name="工号", max_length=8, blank=True)
    realname = models.CharField(verbose_name="真实姓名", max_length=10)
    email = models.EmailField(verbose_name="邮箱", max_length=32)
    phone = models.CharField(verbose_name="手机号", max_length=11)
    gender = models.CharField(verbose_name="性别", max_length=2)
    group = models.ForeignKey(Group, related_name='user_group', verbose_name="用户所属组", on_delete=models.DO_NOTHING)
    rank = models.ForeignKey(Rank, related_name="user_rank", verbose_name="用户职级", on_delete=models.DO_NOTHING)
    role = models.ForeignKey(Role, related_name='user_role', verbose_name="用户角色", on_delete=models.DO_NOTHING)
    id_card = models.CharField(verbose_name="身份证", max_length=20)
    school = models.CharField(verbose_name="毕业学校", max_length=20)
    gradution_time = models.DateField()
    education = models.CharField(verbose_name="学历", max_length=20)
    pre_job = models.CharField(verbose_name="上一份工作", max_length=20)
    entry_time = models.DateField(verbose_name="入职时间")
    birth_day = models.DateField(verbose_name="生日")
    
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.user.username
