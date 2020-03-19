from django.conf.urls import url
from django.urls import path
from .views import CourseListView, PersonCourseListView
from .views import CourseCreateView, PointListView
from .views import CourseDetailView

app_name="training"
urlpatterns = [
    path('course-list/',CourseListView.as_view(), name="course_list"),
    path('course-detail/<int:pk>', CourseDetailView.as_view(), name="course_detail"),
    path('person-course/', PersonCourseListView.as_view(),name="person_course"),
    path('add-course/', CourseCreateView.as_view(), name="add_course"),
    path('point-list/', PointListView.as_view(), name="point_list"),
]
