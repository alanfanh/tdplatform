from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
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
        return render(request, "account/myself.html", {"user":user})

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
