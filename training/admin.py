from django.contrib import admin

# Register your models here.
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("cname", "range", "address", "teacher","course_time")
    list_filter = ("range","teacher__realname")
    search_fields = ("cname", "teacher__realname")
    raw_id_fields = ("teacher",)
    date_hierarchy = "course_time"
    ordering = ['course_time']


class IntegralAdmin(admin.ModelAdmin):
    list_display = ("person","total", "joined", "teached_group")
    search_fileds = ("person__realname")

