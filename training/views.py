from django.shortcuts import get_object_or_404,render
from django.db.models import Q
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
        # paginator = Paginator(courses_list, self.paginate_by)
        # page = self.request.GET.get('page')
        # print(page)
        # try:
        #     course_list = paginator.page(page)
        #     context['current_page'] = int(page)
        #     strat = (context['current_page']-1)*self.paginate_by
        #     context['strat'] = strat
        # except PageNotAnInteger:
        #     course_list = paginator.page(1)
        # except EmptyPage:
        #     course_list = paginator.page(paginator.num_pages)
        # context['course_list'] = course_list
        context['courses_list'] = courses_list
        context['userinfo'] = userinfo
        return context

class CourseCreateView(UserCourseMixin, CreateView):
    # 添加培训课程 类视图
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
        # print(request.POST,form)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.author = self.request.user
            # 获取穿梭框选中的数据
            joined_people = request.POST.get('student-joined')
            # 先保存对象，生成主键ID后才能添加多对多关系数据。
            new_course.save()
            if joined_people != '':
                id_list = joined_people.split(',')
                for id in id_list:
                    new_course.student.add(id)
            # return redirect("training:course_list")
            return render(request, "training/success.html", {"course":new_course})
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
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(courses, limit)
    else:
        paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        course_page = paginator.page(page)
        # 获取当前页面，实现当前页条目序号
        current_page = int(page)
        strat = (current_page-1)*10
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        course_page = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        course_page = paginator.page(paginator.num_pages)
    for course in course_page:
        obj = model_to_dict(course, fields=['id','cname','range','address','course_time','cdescription','teacher'])
        obj['teacher'] = UserInfo.objects.get(id=obj['teacher']).realname
        # 获取参加课程的人数
        obj['number'] = course.student.all().count()
        obj['student'] = []
        for name in course.student.all():
            obj['student'].append(name.realname)
        obj['course_time'] = obj['course_time'].strftime('%Y-%m-%d %H:%M')
        result['data'].append(obj)
    result['count'] = courses.count()
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
        # print(response['Content-Disposition'], file_name)
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
    # 查询每个用户的course_list数据，通过json返回数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    # integrals = Integral.objects.all()
    # for integral in integrals:
    #     obj = model_to_dict(integral, fields=['id','person','total','joined','teached_group','teached'])
    #     user_id = obj['person']
    #     obj['person'] = UserInfo.objects.get(id=user_id).realname
    #     obj['group'] = UserInfo.objects.get(id=user_id).group.name
    #     result['data'].append(obj)
    # result['count'] = integrals.count()
    # print(result)
    all_userinfo = UserInfo.objects.all()
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(all_userinfo, limit)
    else:
        paginator = Paginator(all_userinfo, 10)
    page = request.GET.get('page')
    try:
        user_page = paginator.page(page)
        # 获取当前页面，实现当前页条目序号
        current_page = int(page)
        strat = (current_page-1)*10
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        user_page = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        user_page = paginator.page(paginator.num_pages)
    for user in user_page:
        obj = model_to_dict(user, fields=['realname','group'])
        # 外键关联查询
        obj['group'] = user.group.name
        obj['joined'] = user.get_joined_points()
        obj['teached_group'] = user.get_group_points()
        obj['teached'] = user.get_department_points()
        obj['total'] = obj['joined'] + obj['teached_group'] + obj['teached']
        result['data'].append(obj)
    result['count'] = all_userinfo.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


# 通过select筛选，返回json格式数据
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
        if year != "All":
            courses = courses.filter(course_time__year=year)
    # 分页处理
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(courses, limit)
    else:
        paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        course_page = paginator.page(page)
        # 获取当前页面，实现当前页条目序号
        current_page = int(page)
        strat = (current_page-1)*10
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        course_page = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        course_page = paginator.page(paginator.num_pages)
    for course in course_page:
        obj = model_to_dict(course, fields=['id','cname','range','address','course_time','cdescription','teacher'])
        obj['teacher'] = UserInfo.objects.get(id=obj['teacher']).realname
        # 获取参加课程的人数
        obj['number'] = course.student.all().count()
        obj['course_time'] = obj['course_time'].strftime('%Y-%m-%d %H:%m')
        result['data'].append(obj)
    result['count'] = courses.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii':False})


@login_required(login_url="/account/login")
def filter_point_list(request):
    # 筛选point数据
    result = {"code":0, "msg":"", "count": 0, "data":[]}
    # points = Integral.objects.all()
    # if request.GET.get('group'):
    #     group_id = request.GET.get('group')
    #     if group_id != 0:
    #         group = Group.objects.get(id=group_id)
    #         # 根据用户所属组过滤
    #         points = points.filter(person__group=group)
    # if request.GET.get('year'):
    #     pass
    # for point in points:
    #     obj = model_to_dict(point, fields=['id','person','total','joined','teached_group','teached'])
    #     user_id = obj['person']
    #     obj['person'] = UserInfo.objects.get(id=user_id).realname
    #     obj['group'] = UserInfo.objects.get(id=user_id).group.name
    #     result['data'].append(obj)
    # result['count'] = points.count()
    # print(result)
    all_userinfo = UserInfo.objects.all()
    if request.GET.get('group'):
        group_id = request.GET.get('group')
        if group_id != 0:
            all_userinfo = all_userinfo.filter(group_id=group_id)
    # 分页处理
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(all_userinfo, limit)
    else:
        paginator = Paginator(all_userinfo, 10)
    page = request.GET.get('page')
    try:
        user_page = paginator.page(page)
        # 获取当前页面，实现当前页条目序号
        current_page = int(page)
        strat = (current_page-1)*10
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        user_page = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        user_page = paginator.page(paginator.num_pages)
    for user in user_page:
        obj = model_to_dict(user, fields=['realname', 'group'])
        # 外键关联查询
        obj['group'] = user.group.name
        obj['joined'] = user.get_joined_points()
        obj['teached_group'] = user.get_group_points()
        obj['teached'] = user.get_department_points()
        obj['total'] = obj['joined'] + obj['teached_group'] + obj['teached']
        result['data'].append(obj)
    result['count'] = all_userinfo.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii':False})


@login_required(login_url="/account/login")
def search_course(request):
    result = {"code":0, "msg":"", "count":0, "data":[]}
    if request.GET.get("search"):
        search_key = request.GET.get("search")
        courses = Course.objects.filter(Q(cname__icontains=search_key) | Q(address__icontains=search_key)| Q(teacher__realname__icontains=search_key))
    # 分页及每页条目数
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(courses, limit)
    else:
        paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        course_page = paginator.page(page)
        # 获取当前页面，实现当前页条目序号
        current_page = int(page)
        strat = (current_page-1)*10
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        course_page = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        course_page = paginator.page(paginator.num_pages)
    for course in course_page:
        obj = model_to_dict(course, fields=['id','cname','range','address','course_time','cdescription','teacher'])
        obj['teacher'] = UserInfo.objects.get(id=obj['teacher']).realname
        obj['number'] = course.student.all().count()
        obj['course_time'] = obj['course_time'].strftime('%Y-%m-%d %H:%m')
        result['data'].append(obj)
    result['count'] = courses.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii":False})


# 编辑课程数据
@login_required(login_url="/account/login")
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    this_form = CreateCourseForm(instance=course)
    if request.method == "GET":
        groups = Group.objects.all()
        return render(request, "training/edit_course.html",{"course":course, "groups":groups, "this_form":this_form})
    else:
        # print(request.POST, request.FILES)
        # 生成表单对象，修改为上传的数据
        form = CreateCourseForm(request.POST or None, request.FILES,  instance=course)
        if form.is_valid():
            edit_course = form.save(commit=False)
            # 获取穿梭框选中的数据
            joined_people = request.POST.get('student-joined')
            # 先保存对象，生成主键ID后才能添加多对多关系数据。
            edit_course.save()
            if joined_people != '':
                id_list = joined_people.split(',')
                # 直接修改多对多关系
                edit_course.student.set(id_list)
            else:
                # 清除所有多对多
                edit_course.student.clear()
            return redirect("training:course_list")


# 返回json数据
@login_required(login_url="/account/login")
def get_userinfo(request):
    result = {"data": [], "select":[]}
    users = UserInfo.objects.all()
    for user in users:
        obj = model_to_dict(user, fields=['id', 'realname'])
        result['data'].append(obj)
    # 获取指定course参与的用户id
    if 'id' in request.GET:
        # print('id=', request.GET['id'])
        course = Course.objects.get(id=request.GET['id'])
        for s in course.student.all():
            result['select'].append(s.id)
    return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

# 返回个人培训的json数据
@login_required(login_url="/account/login")
def person_course_data(request):
    result = {"code":0, "msg":"", "count":0, "data":[]}
    user = UserInfo.objects.get(user=request.user)
    courses = Course.objects.filter(teacher=user)
    # 获取url附带的参数，进行数据分页
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(courses, limit)
    else:
        paginator = Paginator(courses, 10)
    page = request.GET.get('page')
    try:
        page_courses = paginator.page(page)
    except PageNotAnInteger:
        page_courses = paginator.page(1)
    except EmptyPage:
        page_courses = paginator.page(paginator.num_pages)
    # 对已分页的数据处理成json
    for course in page_courses:
        obj = model_to_dict(course, fields=['id', 'cname', 'range', 'address','course_time', 'cdescription', 'teacher'])
        obj['teacher'] =  UserInfo.objects.get(id=obj['teacher']).realname
        obj['number'] = course.student.all().count()
        obj['course_time'] = obj['course_time'].strftime('%Y-%m-%d %H:%m')
        result['data'].append(obj)
    result['count'] = courses.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii": False})
