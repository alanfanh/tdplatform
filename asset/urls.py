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
    path('my-tec/', views.my_tec, name="my_tec"),
    path('assigned-list', views.assigned_list, name="assigned_list"),
    # 主页客诉
    path('complaint-list/', views.complaint_list, name="complaint_list"),
    path('complaint-detail/<int:complaint_id>', views.complaint_detail, name="complaint_detail"),
    path('add-complaint/', views.add_complaint, name="add_complaint"),
    # 主页优秀实践
    path('tec-list/', views.tec_list, name="tec_list"),
    path('tec-detail/', views.tec_detail, name="tec_detail"),
    path('add-tec', views.add_tec, name="add_tec"),
]
