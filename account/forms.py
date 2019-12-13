# account Form
from django import forms
from .models import UserInfo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserInfoForm(forms.Form):
    class Meta:
        model = UserInfo
        fields = ()