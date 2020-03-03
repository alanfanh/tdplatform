from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User

class Articles(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING , related_name="user_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)
    
    def __str__(self):
        return self.title

class TecContent(models.Model):
    id = models.AutoField(primary_key=True)
    tname = models.CharField(verbose_name="优秀实践标题", max_length=30)
    tag = models.CharField(verbose_name="标签", max_length=10)
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING, related_name="user_post")
    body = models.TextField(verbose_name="内容概括")
    created_at = models.DateTimeField(verbose_name='时间', auto_now=False, auto_now_add=False, default=timezone.now)
    file = models.FileField(verbose_name="附件", upload_to=None, max_length=100)
    status = models.CharField(verbose_name="状态", max_length=2)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return self.tname


class Complaint(models.Model):
    """客诉记录数据模型"""
    id = models.AutoField(primary_key=True)
    cname = models.CharField(verbose_name="客诉名称", max_length=30)
    type = models.CharField(verbose_name="客诉类型", max_length=10)
    submitter = models.CharField(verbose_name="提交人", max_length=50)
    ctime = models.DateTimeField(verbose_name="客诉时间", auto_now=False, auto_now_add=False)
    product = models.CharField(verbose_name="产品型号", max_length=10)
    version = models.CharField(verbose_name="软件版本", max_length=10)
    NAME_IN_LEVEL_CHOICES = (
        ("high","高"),
        ("mid","中"),
        ("low","低"),
    )
    level = models.CharField(verbose_name="严重程度", max_length=50, choices=NAME_IN_LEVEL_CHOICES)
    product_line = models.CharField(verbose_name="产品线", max_length=20)
    category = models.CharField(verbose_name="问题分类", max_length=10)
    tester = models.CharField(verbose_name="分析责任人", max_length=10)
    complete_time = models.DateTimeField(verbose_name="分析完成时间", auto_now=False, auto_now_add=False)
    status = models.CharField(verbose_name="措施状态", max_length=50)
    cfile = models.FileField(verbose_name="材料附件", upload_to=None, max_length=100)

    def __str__(self):
        return self.cname
    

#     report_file = models.FileField(
#         verbose_name="", upload_to=None, max_length=100)
#     description = models.TextField(verbose_name="问题描述")
#     oa_number = models.CharField(verbose_name="OA流程号", max_length=20)
#     improvement = models.CharField(verbose_name="改进措施", max_length=100)
#     complete_time = models.DateField(verbose_name="措施完成时间", auto_now=False, auto_now_add=False)
#     closed_time = models.DateField(verbose_name="计划闭环时间", auto_now=False, auto_now_add=False)
#     cause = models.CharField(verbose_name="问题根因", max_length=50)
#     problem_point = models.CharField(verbose_name="问题引入点", max_length=20)
#     control_point = models.CharField(verbose_name="问题控制点", max_length=20)
#     analysis = models.CharField(verbose_name="是否分析", max_length="2")
#     effect = models.CharField(verbose_name="客户影响", max_length=20)
#     problem = models.CharField(verbose_name="典型问题", max_length=50)
#     asset_id = models.CharField(verbose_name="资产编号", max_length=50)
#     month = models.CharField(verbose_name="客诉月", max_length=6)
#     area = models.CharField(verbose_name="区域", max_length=4)