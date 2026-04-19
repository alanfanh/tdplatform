"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from account import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('asset/', include('asset.urls', namespace='asset')),
    path('account/', include('account.urls',namespace='account')),
    path('pwd_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('pwd_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('', views.home_page, name='home'), 
    path('home/', views.home_page, name='home'),
    path('home/home-course-list-data', views.home_course_list, name='home_course_list'),
    path('article/', include('article.urls', namespace='article')),
    path('training/', include('training.urls', namespace='training')),
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico'))
]
