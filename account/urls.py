from django.conf.urls import url
from django.urls import path, reverse_lazy
from . import views

from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name="user_login"),
    path('index', views.index, name="index"),
    path('<int:user_id>', views.user_detail, name="user_detail"),
    path('my-information/', views.myself, name="my_information"),
    path('group', views.group_user, name="group_user"),
    # django内置的登录LoginView类
    path('login/', LoginView.as_view(template_name="account/login.html"), name="user_login"),
    path('logout/', LogoutView.as_view(template_name="account/logout.html"), name="user_logout"),
    path('password-change/', PasswordChangeView.as_view(template_name="account/password_change_form.html", success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('password-change-done', PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name='password_change_done'),
]
