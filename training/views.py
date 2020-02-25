from django.shortcuts import get_object_or_404,render

# Create your views here.
from django.views.generic import TemplateView, ListView
from .models import Course, Integral

class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = 'course/course_list.html'
