from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.blog_title,  name="blog_title"),
    path('<int:article_id>', views.blog_article, name="blog_detail")
]
