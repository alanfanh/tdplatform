from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from account.models import Group, UserInfo

class Articles(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(
        User, on_delete=models.DO_NOTHING , related_name="user_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-publish",)
        verbose_name = "技术文章"
        verbose_name_plural = "技术文章"
    
    def __str__(self):
        return self.title

class TecTag(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag

class TecContent(models.Model):
    id = models.AutoField(primary_key=True)
    tname = models.CharField(verbose_name="优秀实践标题", max_length=30)
    tec_tag = models.ManyToManyField(TecTag, verbose_name="类别", related_name="tec_tag", blank=True)
    award = models.CharField(verbose_name="奖项", max_length=50, blank=True)
    group = models.ForeignKey(Group, verbose_name="小组", on_delete=models.DO_NOTHING, related_name="group_tec")
    author = models.ForeignKey(UserInfo, verbose_name="作者", on_delete=models.DO_NOTHING, related_name="user_post")
    body = models.TextField(verbose_name="内容概括")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    file = models.FileField(verbose_name="附件", upload_to="tec_files", max_length=100)
    status = models.CharField(verbose_name="状态", max_length=2)

    class Meta:
        ordering = ("-created_at", )
        verbose_name_plural = "优秀实践"

    def __str__(self):
        return self.tname

    def save(self, *args, **kwargs):
        super(TecContent, self).save(*args, **kwargs)


class NodeMessage(models.Model):
    # 优秀实践审核信息
    id = models.AutoField(primary_key=True)
    name = models.OneToOneField(
        TecContent, verbose_name="优秀实践", on_delete=models.CASCADE)
    pl_name = models.CharField(verbose_name="组长", max_length=50, blank=True)
    pl_decide = models.CharField(verbose_name="组长意见", max_length=50, blank=True)
    pl_notes = models.CharField(verbose_name="组长意见说明", max_length=50, blank=True)
    pl_time = models.DateTimeField(
        verbose_name="组长处理时间", auto_now=False, auto_now_add=False)
    m_name = models.CharField(verbose_name="经理", max_length=50, blank=True)
    m_decide = models.CharField(verbose_name="经理意见", max_length=50, blank=True)
    m_notes = models.CharField(verbose_name="经理意见说明", max_length=50, blank=True)
    m_time = models.DateTimeField(
        verbose_name="经理处理时间", auto_now=False, auto_now_add=False)


class Complaint(models.Model):
    """客诉记录数据模型"""
    id = models.AutoField(primary_key=True)
    cname = models.CharField(verbose_name="客诉名称", max_length=30)
    type = models.CharField(verbose_name="客诉类型", max_length=10)
    submitter = models.CharField(verbose_name="提交人", max_length=50)
    oa_number = models.CharField(verbose_name="OA流程号", max_length=20, blank=True)
    ctime = models.DateTimeField(verbose_name="客诉时间", auto_now=False, auto_now_add=False)
    area = models.CharField(verbose_name="区域", max_length=4, default=None)
    product = models.CharField(verbose_name="产品型号", max_length=10)
    product_line = models.CharField(verbose_name="产品线", max_length=20)
    version = models.CharField(verbose_name="软件版本", max_length=10)
    NAME_IN_LEVEL_CHOICES = (
        ("high","高"),
        ("mid","中"),
        ("low","低"),
    )
    level = models.CharField(verbose_name="严重程度", max_length=50, choices=NAME_IN_LEVEL_CHOICES)
    tester = models.CharField(verbose_name="分析责任人", max_length=10)
    analysis_time = models.DateTimeField(verbose_name="分析完成时间", auto_now=False, auto_now_add=False, blank=True)
    status = models.CharField(verbose_name="措施状态", max_length=50)
    complete_time = models.DateField(verbose_name="措施完成时间", auto_now=False, auto_now_add=False, blank=True)
    category = models.CharField(verbose_name="问题分类", max_length=10)
    cfile = models.FileField(verbose_name="材料附件", upload_to="complaint_file", max_length=100)
    description = models.TextField(verbose_name="问题描述", blank=True)
    created_by = models.ForeignKey(User, verbose_name="创建者", on_delete=models.DO_NOTHING, related_name="user_created")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )
        verbose_name_plural = "客诉记录"

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
