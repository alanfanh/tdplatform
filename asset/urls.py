from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'asset'
urlpatterns = [
    path('<int:article_id>', views.article_content, name="blog_detail"),
    # 
    path('my-complaint/', views.my_complaint, name="my_complaint"),
    path('unprocess-tec/', views.unprocess_tec, name="unprocess_tec"),
    path('process-tec/', views.process_tec, name="process_tec"),
    path('my-tec/', views.my_tec, name="my_tec"),
    path('assigned-list', views.assigned_list, name="assigned_list"),
    path('unprocess-tec-detail/<int:tec_id>', views.unprocess_tec_detail, name="unprocess_tec_detail"),
    path('processed-tec-detail/<int:tec_id>', views.processed_tec_detail, name="processed_tec_detail"),
    # 主页客诉
    path('complaint-list/', views.complaint_list, name="complaint_list"),
    path('complaint-detail/<int:complaint_id>', views.complaint_detail, name="complaint_detail"),
    path('add-complaint/', views.add_complaint, name="add_complaint"),
    # 主页优秀实践
    path('tec-list/', views.tec_list, name="tec_list"),
    path('tec-detail/<int:tec_id>', views.tec_detail, name="tec_detail"),
    path('add-tec/', views.add_tec, name="add_tec"),
    path('download-file/<int:tec_id>', views.download_tec_file, name="down_tec_file"),
    # 处理ajax返回json数据
    path('group_user', views.group_user, name="group_user"),
]
