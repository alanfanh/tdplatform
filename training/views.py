from django.shortcuts import get_object_or_404,render

# Create your views here.
# 本views.py文件不再写视图函数，而是通过类的视图实现功能

from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from .models import Course, Integral
from account.models import UserInfo, Group
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import CreateCourseForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.utils.encoding import escape_uri_path

class UserMixin(object):
    # 筛选teacher为自己的course
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

class CourseCreateView(UserCourseMixin, CreateView):
    fields = ['cname', 'range', 'course_time', 'address',
              'teacher', 'cdescription', 'file_name', 'student']
    template_name = "training/add_course.html"

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView,self).get_context_data(**kwargs)
        context["groups"] = Group.objects.all()
        context['userinfos'] = UserInfo.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = CreateCourseForm(request.POST, request.FILES)
        print(request.POST,form)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.author = self.request.user
            new_course.save()
            return redirect("training:course_list")
        else:
            groups = Group.objects.all()
            userinfos = UserInfo.objects.all()
            return self.render_to_response({"form": form, "userinfos":userinfos, "groups":groups})

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    context_object_name = "courses"
    template_name = 'training/course_list.html'
    login_url = "/account/login/"

    def get_context_data(self, **kwargs):
        kwargs['userinfo'] = UserInfo.objects.get(user=self.request.user)
        return super(CourseListView, self).get_context_data(**kwargs)

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "training/course_detail.html"
    login_url = "/account/login/"

@login_required(login_url="/account/login")
def download_file(request, course_id):
    # 下载课程附件
    course = Course.objects.get(id=course_id)
    if course.file_name == "":
        return HttpResponse('Null')
    else:
        file_name = course.file_name.name.split('/')[1]
        response = FileResponse(course.file_name)
        response['Content-Type'] = "application/octet-stream"
        # 浏览器会导致中文乱码, 进行如下解码
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(
            escape_uri_path(file_name))
        print(response['Content-Disposition'], content, file_name)
    return response

class DeleteCourseView(LoginRequiredMixin, DeleteView):
    model = Course
    login_url = "/account/login/"
    success_url = reverse_lazy("training:course_list")

    def dispatch(self, *args, **kwargs):
        # 通过ajax弹窗删除
        resp = super(DeleteCourseView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result":"ok"}
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        return resp

# 积分视图
class PointListView(LoginRequiredMixin, ListView):
    model = Integral
    context_object_name = "points"
    template_name = "training/point_list.html"
    login_url = "/account/login"
