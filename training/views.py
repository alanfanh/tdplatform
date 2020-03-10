from django.shortcuts import get_object_or_404,render

# Create your views here.
# 本views.py文件不再写视图函数，而是通过类的视图实现功能

from django.views.generic import TemplateView, ListView
from .models import Course, Integral
from account.models import UserInfo

class CourseListView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = 'training/course_list.html'


class UserMixin(object):
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(teacher=UserInfo.objects.get(user=self.request.user))

class UserCourseMixin(UserMixin):
    model = Course

class PersonCourseListView(UserCourseMixin, ListView):
    # 我贡献的培训视图
    context_object_name = "courses"
    template_name = "training/person_course_list.html"

    def get_context_data(self, **kwargs):
        # 获取context传入模版，如下为userinfo
        kwargs['userinfo'] = UserInfo.objects.get(user=self.request.user)
        return super(PersonCourseListView, self).get_context_data(**kwargs)