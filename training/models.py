from django.db import models
# from account.models import UserInfo

# Create your models here.
# 培训管理应用
class Course(models.Model):
    """培训课程"""
    id =  models.AutoField(primary_key=True)
    cname = models.CharField(verbose_name="课程名", max_length=30)
    range = models.CharField(verbose_name="课程范围", max_length=50)
    course_time = models.DateTimeField(verbose_name="培训时间", auto_now=False, auto_now_add=False)
    address = models.CharField(verbose_name="培训地点", max_length=30)
    teacher = models.ForeignKey(to="account.UserInfo", related_name="course_teacher",verbose_name="主讲人", on_delete=models.DO_NOTHING)
    file_name = models.FileField(verbose_name="附件", upload_to="course_files", max_length=100)
    cdescription = models.CharField(verbose_name="课程概述",max_length=150, blank=True)
    # 多对多，培训课程与参加人
    student = models.ManyToManyField(to="account.UserInfo", related_name="course_joined", blank=True)

    class Meta:
        ordering = ('-course_time',)
        verbose_name = '培训课程'
        verbose_name_plural = '培训课程'

    def __str__(self):
        return self.cname

class Integral(models.Model):
    """培训积分"""
    id = models.AutoField(primary_key=True)
    # 积分表与用户应该是一对一关系
    person = models.ForeignKey(to="account.UserInfo", verbose_name="姓名", on_delete=models.CASCADE, related_name='person_integral')
    total = models.IntegerField(verbose_name="总积分")
    joined = models.IntegerField(verbose_name="参加培训积分")
    teached_group = models.IntegerField(verbose_name="组织小组培训积分")
    teached = models.IntegerField(verbose_name="组织部门培训积分")

    class Meta:
        ordering = ("total",)
