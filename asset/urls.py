from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'asset'
urlpatterns = [
    path('<int:article_id>', views.article_content, name="blog_detail"),
    # 
    path('my-complaint/', views.my_complaint, name="my_complaint"),
    path('my-complaint-data/', views.my_complaint_data, name="my_complaint_data"),
    path('unprocess-tec/', views.unprocess_tec, name="unprocess_tec"),
    path('process-tec/', views.process_tec, name="process_tec"),
    path('my-tec/', views.my_tec, name="my_tec"),
    path('filter-status-myteclist/', views.filter_status_myteclist, name="filter_status_myteclist"),
    path('assigned-list', views.assigned_list, name="assigned_list"),
    path('assigned-list-data/', views.assigned_list_data, name="assigned_list_data"),
    path('unprocess-tec-detail/<int:tec_id>', views.unprocess_tec_detail, name="unprocess_tec_detail"),
    path('processed-tec-detail/<int:tec_id>', views.processed_tec_detail, name="processed_tec_detail"),
    path('my-process-tec/<int:tec_id>', views.my_process_tec, name="my_process_tec"),
    # 主页客诉
    path('complaint-list/', views.complaint_list, name="complaint_list"),
    path('complaint-detail/<int:complaint_id>', views.complaint_detail, name="complaint_detail"),
    path('add-complaint/', views.add_complaint, name="add_complaint"),
    path('download-cfile/<int:complaint_id>', views.download_cfile, name="download_cfile"),
    path('delete-complaint/<int:complaint_id>', views.delete_complaint, name="delete_complaint"),
    path('edit-complaint/<int:complaint_id>', views.edit_complaint, name="edit_complaint"),
    # 主页优秀实践
    path('tec-list/', views.tec_list, name="tec_list"),
    path('tec-detail/<int:tec_id>', views.tec_detail, name="tec_detail"),
    path('add-tec/', views.add_tec, name="add_tec"),
    path('download-file/<int:tec_id>', views.download_tec_file, name="down_tec_file"),
    # 处理ajax返回json数据
    path('group-user/', views.group_user, name="group_user"),
    path('tec-list-data/', views.tec_list_data, name="tec_list_data"),
    path('complaint-list-data/', views.complaint_list_data, name="complaint_list_data"),
    path('filter-tec-range/', views.filter_tec_range, name="filter_tec_range"),
    path('filter-complaint-list/', views.filter_complaint_list, name="filter_complaint_list"),
    path('search-tec/', views.search_tec, name="search_tec"),
    path('search-complaint/', views.search_complaint, name="search_complaint"),
    path('check-tec/', views.check_tec, name="check_tec"),
    path('my-tec-data/', views.my_tec_data, name="my_tec_data"),
    path('process-tec-data/', views.process_tec_data, name="process_tec_data"),
    path('filter-tec-status/', views.filter_tec_status, name="filter_tec_status"),
    # 专利
    path('patent-list/', views.patent_list, name="patent_list"),
    path('patent-list-data/', views.patent_list_data, name="patent_list_data"),
]
