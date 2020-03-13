from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Articles, TecContent, Complaint
from account.models import UserInfo, Role, Group

from django.http import HttpResponse

@login_required(login_url="/account/login")
def article_title(request):
    blogs = Articles.objects.all()
    return render(request, "asset/titles.html", {"blogs": blogs})

@login_required(login_url="/account/login")
def article_content(request, article_id):
    # article = Articles.objects.get(id=article_id)
    article = get_object_or_404(Articles, id=article_id)
    pub = article.publish
    return render(request, "asset/content.html", {"article":article, "publish":pub})


# 资产应用视图函数
# 客诉

@login_required(login_url="/account/login")
def my_complaint(request):
    # 我添加的客诉
    userinfo = UserInfo.objects.get(user=request.user)
    return render(request,"asset/pl_complaint_list.html",{"userinfo":userinfo})

@login_required(login_url="/account/login")
def assigned_list(request):
    # 指派给ste、te的客诉
    userinfo = UserInfo.objects.get(user=request.user)
    return render(request, "asset/assigned_list.html", {"userinfo":userinfo})

# 优秀实践

@login_required(login_url="/account/login")
def unprocess_tec(request):
    # 未处理的优秀实践
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        # PL用户
        tec_list = TecContent.objects.filter(status="1")
        return render(request, "asset/unprocess_pl.html",{"userinfo":userinfo, "tec_list":tec_list})
    elif role.role_name == "M":
        # M用户
        tec_list = TecContent.objects.filter(status="2")
        return render(request, "asset/unprocess_m.html", {"userinfo":userinfo,"tec_list":tec_list})
    else:
        return HttpResponse('Not Found')

@login_required(login_url="account/login")
def process_tec(request):
    # 已处理的优秀实践
    userinfo =  UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        tec_list = TecContent.objects.filter()
        return render(request, "asset/processed_pl.html",{"userinfo":userinfo, "tec_list":tec_list})
    elif role.role_name == "M":
        return render(request, "asset/processed_m.html", {"userinfo":userinfo})
    else:
        return HttpResponse("Not Found")

@login_required(login_url="/account/login")
def my_tec(request):
    # STE添加的优秀实践
    userinfo = UserInfo.objects.get(user=request.user)
    return render(request, "asset/my_tec.html", {"userinfo":userinfo})