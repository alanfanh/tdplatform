from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView
from .models import Course

class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = 'course/course_list.html'