from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Articles, TecContent, Complaint
from account.models import UserInfo, Role, Group

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

@login_required(login_url="/account/login")
def complaint_list(request):
    complaints = Complaint.objects.all()
    userinfo = UserInfo.objects.get(user=request.user)
    return render(request, "asset/complaint_list.html", {"complaints":complaints,"userinfo":userinfo})

@login_required(login_url="/account/login")
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint,id=complaint_id)
    return render(request, "asset/complaint_detail.html", {"complaint":complaint})

@login_required(login_url="/account/login")
def add_complaint(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "asset/add_complaint.html")

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

@login_required(login_url="/account/login")
def tec_list(request):
    # 主页优秀实践列表
    userinfo = UserInfo.objects.get(user=request.user)
    tecs = TecContent.objects.filter(status="3")
    return render(request, "asset/tec_list.html", {"tecs":tecs,"userinfo":userinfo})

@login_required(login_url="/account/login")
def tec_detail(request):
    # 主页优秀时间详情
    # tec = TecContent.objects.get(id=tec_id)
    return render(request, "asset/tec_detail.html")

@login_required(login_url="/account/login")
@csrf_exempt
def add_tec(request):
    if request.method == "POST":
        pass
    else:
        groups = Group.objects.all()
        return render(request,"asset/add_tec.html",{"groups":groups})
