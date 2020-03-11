from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'asset'
urlpatterns = [
    path('', views.article_title,  name="blog_title"),
    path('<int:article_id>', views.article_content, name="blog_detail"),
    # 
    path('my-complaint/', views.my_complaint, name="my_complaint"),
    path('unprocess-tec/', views.unprocess_tec, name="unprocess_tec"),
    path('process-tec/', views.process_tec, name="process_tec"),
]
