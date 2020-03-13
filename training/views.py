from django.shortcuts import get_object_or_404,render

# Create your views here.
# 本views.py文件不再写视图函数，而是通过类的视图实现功能

from django.views.generic import TemplateView, ListView, CreateView
from .models import Course, Integral
from account.models import UserInfo
from braces.views import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import CreateCourseForm


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = "courses"
    template_name = 'training/course_list.html'
    login_url = "/account/login/"

    def get_context_data(self, **kwargs):
        kwargs['userinfo'] = UserInfo.objects.get(user=self.request.user)
        return super(CourseListView, self).get_context_data(**kwargs)

class UserMixin(object):
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(teacher=UserInfo.objects.get(user=self.request.user))

class UserCourseMixin(UserMixin, LoginRequiredMixin):
    model = Course
    login_url="/account/login/"

class PersonCourseListView(UserCourseMixin, ListView):
    # 我贡献的培训视图
    context_object_name = "courses"
    template_name = "training/person_course_list.html"

    def get_context_data(self, **kwargs):
        # 获取context传入模版，如下为userinfo
        kwargs['userinfo'] = UserInfo.objects.get(user=self.request.user)
        kwargs['course_list'] = Course.objects.filter(teacher=kwargs['userinfo'])
        return super(PersonCourseListView, self).get_context_data(**kwargs)

class CourseCreateView(CreateView):
    model = Course
    fields = ['cname', 'range', 'course_time', 'address', 'teacher','file_name']
    template_name = "training/add_course.html"

    def Post(self, request, *args, **kwargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.author = self.request.user
            new_course.save()
            return redirect("training:course_list")
        return self.render_to_response({"form":form})
