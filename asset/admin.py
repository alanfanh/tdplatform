from django.contrib import admin

# Register your models here.
from .models import Articles, TecContent, Complaint


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publish")
    list_filter = ("publish", "author")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ['publish','author']

@admin.register(TecContent)
class TecContentAdmin(admin.ModelAdmin):
    list_display = ("tname", "body", "group", "author", "created_at")
    list_filter = ("group", "created_at")
    # 搜索字段指定了外键，需要指定外键名字
    # 如author__realname
    search_fields = ("tname", "author__realname", )
    date_hierarchy = "created_at"
    ordering = ['created_at',]

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("cname", "type", "submitter", "area", "product", "version","product_line", "level", "ctime", "tester", "status")
    list_filter = ("cname", "area", "product_line", "category", "created_at")
    search_fields = ("cname", "submitter", "product", "tester")
    date_hierarchy = "created_at"
    ordering = ['created_at',"ctime","complete_time"]

