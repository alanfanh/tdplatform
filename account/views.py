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

@loging_required(login_url="login/")
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
                new_user.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        user_post_form = UserInfoForm()
        return render(request, "account/add_user.html",{"user_post_form":user_post_form})