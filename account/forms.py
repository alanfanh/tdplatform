# account Form
from django import forms
from .models import UserInfo

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': u'请输入用户名', }))
    password = forms.CharField(
        error_messages={'required': u'密码不能为空'}, widget=forms.PasswordInput)

class UserInfoForm(forms.Form):
    class Meta:
        model = UserInfo
        fields = ("user", "realname", "email", "phone", "gender", "group", "engineer", "role")
