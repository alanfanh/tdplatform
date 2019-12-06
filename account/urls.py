from django.conf.urls import url
from django.urls import path
from . import views

from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name="user_login"),
    # django内置的登录LoginView类
    path('login/', LoginView.as_view(template_name="account/login.html"), name="user_login"),
    path('logout/', LogoutView.as_view(template_name="account/logout.html"), name="user_logout")
]
