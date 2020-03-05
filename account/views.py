from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm,UserInfoForm
from .models import UserInfo, Group, Role, Rank


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

@login_required(login_url='/login')
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
