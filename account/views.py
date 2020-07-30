from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import LoginForm,UserInfoForm
from .models import UserInfo, Group, Role, Rank
from asset.models import TecContent, Complaint
from training.models import Course
import json
from django.contrib.auth.forms import PasswordChangeForm
from django.forms.models import model_to_dict
from account.models import CommonLinks

@login_required(login_url="/account/login/")
def index(request):
    if request.method == "GET":
        users = UserInfo.objects.all()
        return render(request, 'account/index.html', {'users':users})

def user_login(request):
    # 登录验证
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            # 与数据库中的用户进行比对
            user = authenticate(username=username, password=password)
            if user is not None:  # 通过验证
                login(request, user)
                # print("登陆成功！")
                data={'res':1}                
            else:
                # print("用户名密码错误！！！")
                data={'res':0}                
            response = HttpResponse(json.dumps(data),content_type="application/json")
            # 调用delete_cookie("unproc_num_cookie")删除cookie 
            response.delete_cookie("unproc_num_cookie")
            return response
    else:
        return render(request, 'account/login.html')

@login_required(login_url="/account/login/")
def user_detail(request, user_id):
    user_info = get_object_or_404(UserInfo, id=user_id)
    return render(request, 'account/user_detail.html', {'userinfo': user_info})

@login_required(login_url="/account/login/")
def myself(request):
    user = User.objects.get(username=request.user.username)
    form = PasswordChangeForm(request.user)
    # userinfo = UserInfo.objects.get()
    # if user.is_superuser != 1:
    userinfo = UserInfo.objects.get(user=user)
    role = Role.objects.get(id=userinfo.role_id)
    return render(request,"account/myself.html",{"user":user,"userinfo":userinfo,"form":form})
    # else:
    #     return render(request, "account/myself_admin.html", {"user":user})


@login_required(login_url="/account/login/")
def group_user(request):
    #我的小组
    user = User.objects.get(username=request.user.username)
    if user.is_superuser != 1:
        userinfo = UserInfo.objects.get(user=user)
        group = Group.objects.get(id=userinfo.group_id)
        role = Role.objects.get(id=userinfo.role_id)
        if role.role_name == "PL":
            users = UserInfo.objects.filter(group_id=userinfo.group_id)
            #每页显示10条
            paginator = Paginator(users, 10)
            page = request.GET.get('page')
            try:
                groupnum = paginator.page(page)
                # 获取当前页面，实现当前页条目序号
                current_page = int(page)
                strat = (current_page-1)*10
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                groupnum = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                groupnum = paginator.page(paginator.num_pages)
            template_view = "account/my_group.html"
            groups = Group.objects.all()
            return render(request, template_view, {"users": users, "userinfo": userinfo,"groupnum": groupnum})
    else:
        return HttpResponse("404")


@login_required(login_url="/account/login/")
def group_list(request):
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "M":
        users = UserInfo.objects.filter(group_id=userinfo.group_id)
        #每页显示10条
        paginator = Paginator(users, 10)
        page = request.GET.get('page')
        try:
            groupnum = paginator.page(page)
        # 获取当前页面，实现当前页条目序号
            current_page = int(page)
            strat = (current_page-1)*10
        except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
            groupnum = paginator.page(1)
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            groupnum = paginator.page(paginator.num_pages)
        template_view = "account/group_list.html"
        groups = Group.objects.all()
        return render(request, template_view, {"groups":groups,"userinfo":userinfo,"users":users,"groupnum": groupnum})
    else:
        return HttpResponse('404')


@login_required(login_url="/account/login/")
def all_user(request):
    """查看所有用户，显示用户信息列表"""
    user=User.objects.get(username=request.user.username)
    groups = Group.objects.all()
    ranks = Rank.objects.all()
    roles = Role.objects.all()
    if user.is_superuser == 1:
        user_info = UserInfo.objects.all()
        return render(request, "account/user_list.html", {"user_info":user_info,"groups":groups,"ranks":ranks,"roles":roles})
    else:
        userinfo = UserInfo.objects.get(user=user)
        role = Role.objects.get(id=userinfo.role_id)
        if role.role_name == "M":
            user_info = UserInfo.objects.all()
            return render(request,"account/user_list.html",{"user_info":user_info,"groups":groups,"ranks":ranks,"roles":roles})
        else:
            return HttpResponse("404 not found")


@login_required(login_url="/account/login/")
@csrf_exempt
def add_user(request):
    """添加新用户"""
    if request.method == "POST":
        user_post_form = UserInfoForm(data=request.POST)
        print(user_post_form, request.POST)
        if user_post_form.is_valid():
            cd = user_post_form.cleaned_data
            try:
                new_user = user_post_form.save(commit=False)
                new_user.user = request.user
                new_user.realname = request.realname
                new_user.email= request.email
                new_user.phone = request.phone
                new_user.group = request.group
                new_user.engineer = request.engineer
                new_user.role = request.role
                new_user.id_card = request.id_card
                new_user.school = request.school
                new_user.gradution_time = request.gradution_time
                new_user.education = request.education
                new_user.pre_job = request.pre_job
                new_user.entry_time = request.entry_time
                new_user.birth_day = request.birth_day
                new_user.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        user_post_form = UserInfoForm()
        user_roles = Role.objects.all()
        user_ranks = Rank.objects.all()
        user_groups = Group.objects.all()
        return render(request, "account/add_user.html",{"user_post_form":user_post_form,"user_roles":user_roles,"user_ranks":user_ranks,"user_groups":user_groups})

@login_required(login_url='/account/login')
@csrf_exempt
def redit_user(request,user_id):
    # 编辑用户信息
    user=User.objects.get(username=request.user.username)
    if user.is_superuser == 1:
        if request.method == "GET":
            # 获取需要修改的user对象，实例化
            userinfo = UserInfo.objects.get(id=user_id)
            user_roles = Role.objects.all()
            user_ranks = Rank.objects.all()
            user_groups = Group.objects.all()
            this_user_form = UserInfoForm(initial={"realname":userinfo.realname,"email":userinfo.email,"phone":userinfo.phone,"gender":userinfo.gender})
            return render(request, "account/redit_user.html", {"user_form": this_user_form, "userinfo": userinfo, "user_roles":user_roles, "user_ranks":user_ranks, "user_groups":user_groups})
        else:
            redit_userinfo = UserInfo.objects.get(id=user_id)
            redit_user = User.objects.get(username=redit_userinfo)
            # print(request.POST)
            try:
                redit_userinfo.realname = request.POST['realname']
                redit_userinfo.gender = request.POST['gender']
                redit_userinfo.role = Role.objects.get(
                    id=request.POST['role_id'])
                redit_userinfo.rank = Rank.objects.get(
                    id=request.POST['rank_id'])
                redit_userinfo.group = Group.objects.get(
                    id=request.POST['group_id'])
                # 同步邮箱
                redit_userinfo.email = request.POST['email']
                redit_user.email = redit_userinfo.email
                # 修改用户名username
                redit_user.username = request.POST['username']
                redit_userinfo.phone = request.POST['phone']
                redit_userinfo.education = request.POST['education']
                redit_userinfo.school = request.POST['school']
                redit_userinfo.pre_job = request.POST['pre_job']
                redit_userinfo.id_card = request.POST['id_card']
                # redit_user.birth_day = request.POST['birth_day']
                redit_user.save()
                redit_userinfo.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
    else:
        raise HttpResponse("404")


@login_required(login_url="/account/login")
@csrf_exempt
@require_POST
def change_pwd(request):
    form = PasswordChangeForm(user=request.user,data=request.POST)
    print(form.errors)
    if form.is_valid():
        username = request.user.username
        oldpwd = request.POST.get('old_password')
        user = authenticate(username=username,password=oldpwd)
        if user is not None and  user.is_active:
            print('***OK***')
            newpassword = request.POST.get('new_password1')
            user.set_password(newpassword)
            user.save()
            return HttpResponse("1")
    else:
        return HttpResponse(form.errors)


# 首页视图渲染
@login_required(login_url="/account/login")
@csrf_exempt
def home_page(request):
    # 查询数据中心
    courses = Course.objects.all()
    tecs = TecContent.objects.filter(status="3")
    coms = Complaint.objects.all()

    #获取常用链接表单
    links = CommonLinks.objects.order_by('-click_number')

    # 获取最近培训数据
    last_courses = Course.objects.filter().order_by('-course_time')[:4]
    # files = Course.objects.filter().order_by('-course_time')[:5]
    # 未处理的优秀实践
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    unproc_num = ''
    if role.role_name == "PL":
        # PL用户
        tec_list = TecContent.objects.filter(status="1", group_id=userinfo.group_id)
        unproc_num = tec_list.count()
    elif role.role_name == "M":
        # M用户
        tec_list = TecContent.objects.filter(status="2")
        unproc_num = tec_list.count()
    else:
        return render(request, "home.html", {"courses": courses, "tecs": tecs, "coms": coms, "last_courses": last_courses, "links": links})
    # print(tec_num)
    # rsp = render(request, "home.html", {"courses": courses, "tecs": tecs, "coms": coms, "last_courses": last_courses, "files": files, "tec_num": tec_num})
        unproc_num = ''
    rsp = render(request, "home.html", {"courses": courses, "tecs": tecs, "coms": coms, "last_courses": last_courses, "links":links})
    rsp.set_cookie("unproc_num_cookie",unproc_num, path='/')
    return rsp

@login_required(login_url="/account/login")
@csrf_exempt
def home_course_list(request):
    result = {"count": 5, "data": []}
    if request.GET.get('range'):        
        range = request.GET.get('range')
        # 数据查询
        if range == "0":
            files = Course.objects.filter().order_by('-course_time')[:5]
        else:            
            files = Course.objects.filter(range=range)[:5]        
        # 数据转换
        for file in files:
            obj = model_to_dict(file, fields=['id','cname','range','course_time','file_name'])
            obj['file_name'] = str(obj['file_name'])            
            try:
                obj['course_time'] = obj['course_time'].strftime('%Y-%m-%d')                    
            except:
                pass
            result['data'].append(obj)
        result['count'] = files.count()        
        return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

#跳转至外部链接后 链接点击数目增加
@login_required(login_url="/account/login")
@csrf_exempt
def click_number_add(request):
    linksname = request.POST.get('linksname')
    testlink = CommonLinks.objects.get(id=1)
    bugfree = CommonLinks.objects.get(id=2)
    eoa = CommonLinks.objects.get(id=3)
    oa = CommonLinks.objects.get(id=4)
    management_platform = CommonLinks.objects.get(id=5)
    agile = CommonLinks.objects.get(id=6)
    attendance = CommonLinks.objects.get(id=7)
    linksname = linksname.strip()
    if linksname == 'testlink':
        testlink.click_number += 1
        testlink.save()
    elif linksname == 'bugfree':

        bugfree.click_number += 1
        bugfree.save()
    elif linksname == 'eoa':
        eoa.click_number += 1
        eoa.save()
        return JsonResponse({'res': 3})
    elif linksname == '旧oa':
        oa.click_number += 1
        oa.save()
    elif linksname == '资产设备管理平台':
        management_platform.click_number += 1
        management_platform.save()
    elif linksname == 'Agile平台':
        agile.click_number += 1
        agile.save()
    elif linksname == '考勤查询':
        attendance.click_number += 1
        attendance.save()
    return JsonResponse({'res': 1})
