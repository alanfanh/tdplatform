from django.conf.urls import url
from django.urls import path
from .views import CourseListView, PersonCourseListView
from .views import CourseCreateView, PointListView
from .views import CourseDetailView, DeleteCourseView
from . import views

app_name="training"
urlpatterns = [
    path('course-list/',CourseListView.as_view(), name="course_list"),
    path('course-detail/<int:pk>', CourseDetailView.as_view(), name="course_detail"),
    path('person-course/', PersonCourseListView.as_view(), name="person_course"),
    path('add-course/', CourseCreateView.as_view(), name="add_course"),
    path('download-coursefile/<int:course_id>', views.download_file, name="download_file"),
    path('delete-course/<int:pk>', DeleteCourseView.as_view(), name="delete_course"),
    # 积分表
    path('point-list/', PointListView.as_view(), name="point_list"),
    # 处理ajax返回json数据
    path('course-list-data/', views.course_list_data, name="course_list_data"),
    path('point-list-data/', views.point_list_data, name="point_list_data"),
    path('filter-course-list/', views.filter_course_list, name="filter_course_list"),
    path('filter-point-list/' ,views.filter_point_list, name="filter_point_list"),
    path('search-course/', views.search_course, name="search_course"),
    path('edit-course/<int:course_id>', views.edit_course, name="edit_course"),
    path('get-userinfo/', views.get_userinfo, name="get_userinfo"),
    path('person-course-data/', views.person_course_data, name="perison_course_data"),
]
