from django.contrib import admin

# Register your models here.
from .models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user","realname")
    list_filter = ("group")