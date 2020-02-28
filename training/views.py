from django.shortcuts import get_object_or_404,render

# Create your views here.
# 本views.py文件不再写视图函数，而是通过类的视图实现功能

from django.views.generic import TemplateView, ListView
from .models import Course, Integral

class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = 'training/course_list.html'
