from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm,UserInfoForm
from .models import UserInfo, Group, Role


@login_required(login_url="login/")
def index(request):
    if request.method == "GET":
        users = UserInfo.objects.all()
        return render(request, 'account/index.html', {'users':users})

@login_required(login_url="login/")
def user_detail(request, user_id):
    user_info = get_object_or_404(UserInfo, id=user_id)
    return render(request, 'account/user_detail.html', {'userinfo': user_info})

@login_required(login_url="login/")
def myself(request):
    user = User.objects.get(username=request.user.username)
    if user.is_superuser != 1:
        userinfo = UserInfo.objects.get(user=user)
        return render(request, "account/myself.html", {"user":user, "userinfo":userinfo})
    else:
        return render(request, "account/myself_admin.html", {"user":user})

@login_required(login_url="login/")
def group_user(request):
    user = User.objects.get(username=request.user.username)
    if user.is_superuser != 1:
        userinfo = UserInfo.objects.get(user=user)
        group = Group.objects.get(id=userinfo.group_id)
        role = Role.objects.get(id=userinfo.role_id)
        if role.role_name == "PL":
            users = UserInfo.objects.filter(group_id=userinfo.group_id)
            groups = Group.objects.all()
            return render(request, 'account/group_user.html', {"users":users, "groups":groups})


@login_required(login_url="login/")
def all_user(request):
    """查看所有用户，显示用户信息列表"""
    user=User.objects.get(username=request.user.username)
    if user.is_superuser == 1:
        user_info = UserInfo.objects.all()
        return render(request, "account/user_list.html", {"user_info":user_info})
    else:
        userinfo = UserInfo.objects.get(user=user)
        role = Role.objects.get(id=userinfo.role_id)
        if role.role_name == "M":
            user_info = UserInfo.objects.all()
            return render(request,"account/user_list.html",{"user_info":user_info})
        else:
            return HttpResponse("404 not found")


@login_required(login_url="login/")
@csrf_exempt
def add_user(request):
    """添加新用户"""
    if request.method == "POST":
        user_post_form = UserInfoForm(data=request.post)
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
        return render(request, "account/add_user.html",{"user_post_form":user_post_form})