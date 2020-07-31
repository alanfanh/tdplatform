from django.contrib import admin

# Register your models here.
from .models import UserInfo, Group, Role


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user","realname","job_num","group", "rank", "email", "gender", "role")
    list_filter = ("group",)
    search_fields = ("user__username","realname", "group__name")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name","pl")
    list_filter = ("name", "pl")
    search_fields = ("name", "pl")


class RoleAdmin(admin.ModelAdmin):
    list_display = ("role_name",)
    list_filter = ("role_name",)
    search_fields = ("role_name",)


# 将role注册到管理后台
admin.site.register(Role, RoleAdmin)


# 更改后台管理的标题
admin.site.site_title = "内部平台后台管理"
admin.site.site_header = "平台后台管理"
admin.site.index_title = "后台管理"
