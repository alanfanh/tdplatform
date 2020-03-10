from django.conf.urls import url
from django.urls import path
from .views import CourseListView, PersonCourseListView

app_name="training"
urlpatterns = [
    path('course-list/',CourseListView.as_view(), name="course_list"),
    path('person-course/', PersonCourseListView.as_view(),name="person_course")
]
