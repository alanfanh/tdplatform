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
    return render(request, 'account/user_detail.html', {})

@login_required(login_url="login/")
def myself(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user":user, "userinfo":userinfo})
