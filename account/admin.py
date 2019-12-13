from django.contrib import admin

# Register your models here.
from .models import UserInfo, Group, Role

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user","realname","group", "email", "gender", "role")
    list_filter = ("group",)
    search_fields = ("user", "realname", "group")


admin.site.register(UserInfo, UserInfoAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display = ("name","pl")
    list_filter = ("name", "pl")
    search_fields = ("name", "pl")

admin.site.register(Group, GroupAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ("role_name",)
    list_filter = ("role_name",)
    search_fields = ("role_name",)

admin.site.register(Role, RoleAdmin)
