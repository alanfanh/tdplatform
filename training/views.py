from django.shortcuts import get_object_or_404,render
import json
# Create your views here.
# 本views.py文件不再写视图函数，而是通过类的视图实现功能
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from .models import Course, Integral
from account.models import UserInfo, Group
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import CreateCourseForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse,JsonResponse
from django.utils.encoding import escape_uri_path
from django.forms.models import model_to_dict

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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # 获取context传入模版，如下为userinfo
        context = super(PersonCourseListView, self).get_context_data(**kwargs)
        userinfo = UserInfo.objects.get(user=self.request.user)
        courses_list = Course.objects.filter(teacher=userinfo)
        paginator = Paginator(courses_list, self.paginate_by)
        page = self.request.GET.get('page')
        print(page)
        try:
            course_list = paginator.page(page)
            context['current_page'] = int(page)
            strat = (context['current_page']-1)*self.paginate_by
            context['strat'] = strat
        except PageNotAnInteger:
            course_list = paginator.page(1)
        except EmptyPage:
            course_list = paginator.page(paginator.num_pages)
        context['course_list'] = course_list
        context['courses_list'] = courses_list
        context['userinfo'] = userinfo
        return context

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

@login_required(login_url="/account/login")
def course_list_data(request):
    # 返回course_list的json数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    courses = Course.objects.all()
    for course in courses:
        obj = model_to_dict(course, fields=['id','cname','range','address','course_time','cdescription','teacher'])
        obj['teacher'] = UserInfo.objects.get(id=obj['teacher']).realname
        result['data'].append(obj)
    result['count'] = courses.count()
    print(result)
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


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
        print(response['Content-Disposition'], file_name)
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

@login_required(login_url="/account/login")
def point_list_data(request):
    # 返回course_list的json数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    integrals = Integral.objects.all()
    for integral in integrals:
        obj = model_to_dict(integral, fields=['id','person','total','joined','teached_group','teached'])
        user_id = obj['person']
        obj['person'] = UserInfo.objects.get(id=user_id).realname
        obj['group'] = UserInfo.objects.get(id=user_id).group.name
        result['data'].append(obj)
    result['count'] = integrals.count()
    print(result)
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


# 返回json格式数据
@login_required(login_url="/account/login")
def filter_course_list(request):
    # 筛选course数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    courses = Course.objects.all()
    if request.GET.get('range'):
        range = request.GET.get('range')
        courses = courses.filter(range=range)
    if request.GET.get('year'):
        year = request.GET.get('year')
        courses = courses.filter(course_time__year=year)
    for course in courses:
        obj = model_to_dict(course, fields=['id','cname','range','address','course_time','cdescription','teacher'])
        # 获取参加课程的人数
        obj['number'] = course.student.all().count()
        result['data'].append(obj)
    result['count'] = courses.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii':False})
