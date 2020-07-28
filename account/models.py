from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from training.models import Course

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

    def get_joined_points(self):
        # 类方法，返回该User参加的培训的积分
        course = Course.objects.filter(student=self.user.userinfo).exclude(teacher_id=self.id)
        point = course.count() * 1
        return point

    def get_group_points(self):
        # 类方法，返回该User主持小组的培训的积分
        course = Course.objects.filter(teacher_id=self.id).exclude(range="测试部")
        return course.count() * 2

    def get_department_points(self):
        # 类方法，返回该user主持部门的培训的积分
        course = Course.objects.filter(teacher_id=self.id, range="测试部")
        return course.count() * 2

class CommonLinks(models.Model):
    """
    常用网站点击次数统计表
    """
    id = models.AutoField(primary_key=True)
    links_name = models.CharField(verbose_name="常用链接",max_length=30)
    click_number = models.IntegerField(verbose_name="点击次数",default=0)
    url = models.CharField(verbose_name="url地址",max_length=100,default=0)
    class Meta:
        verbose_name = "常用链接"
        verbose_name_plural = "常用链接"