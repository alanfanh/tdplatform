from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Articles, TecContent, Complaint, TecTag, NodeMessage
from account.models import UserInfo, Role, Group

from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import TecContentForm, ComplaintForm

from django.core import serializers
from django.forms.models import model_to_dict
from django.utils.encoding import escape_uri_path

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
    complaints = Complaint.objects.filter(created_by=request.user)
    return render(request, "asset/pl_complaint_list.html", {"userinfo": userinfo, "complaints": complaints})

@login_required(login_url="/account/login")
def assigned_list(request):
    # 指派给ste、te的客诉
    userinfo = UserInfo.objects.get(user=request.user)
    complaints = Complaint.objects.filter(tester=userinfo.realname)
    return render(request, "asset/assigned_list.html", {"userinfo":userinfo, "complaints":complaints})

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
def download_cfile(request, complaint_id):
    # 下载客诉附件
    com = get_object_or_404(Complaint, id=complaint_id)
    if com.file != "":
        file_name = com.cfile.name.split('/')[1]
        response = FileResponse(com.cfile)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(
            escape_uri_path(file_name))
        return response
    else:
        return HttpResponse("null") 

@login_required(login_url="/account/login")
def add_complaint(request):
    # 添加客诉信息
    form = ComplaintForm(request.POST, request.FILES)
    if request.method == "POST":
        print(form)
        if form.is_valid():
            new_complaint = form.save(commit=False)
            new_complaint.created_by = request.user
            new_complaint.save()
            return redirect("asset:complaint_list")
        else:
            return HttpResponse('3')
    else:
        return render(request, "asset/add_complaint.html", {"form":form})

# 优秀实践

@login_required(login_url="/account/login")
def unprocess_tec(request):
    # 未处理的优秀实践
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        # PL用户
        tec_list = TecContent.objects.filter(status="1", group_id=userinfo.group_id)
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
        tec_list = TecContent.objects.filter(group_id=userinfo.group_id).exclude(status="1")
        return render(request, "asset/processed_pl.html",{"userinfo":userinfo, "tec_list":tec_list})
    elif role.role_name == "M":
        tec_list = TecContent.objects.exclude(status="2")
        return render(request, "asset/processed_m.html", {"userinfo":userinfo, "tec_list":tec_list})
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
def tec_detail(request, tec_id):
    # 主页优秀时间详情
    tec = get_object_or_404(TecContent, id=tec_id)
    return render(request, "asset/tec_detail.html", {"tec":tec})

@login_required(login_url="/account/login")
@csrf_exempt
def add_tec(request):
    # 添加优秀实践
    form = TecContentForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            new_tec = form.save(commit=False)
            new_tec.status = "1"
            # new_tec.author = UserInfo.objects.get(id=request.POST['author'])
            # new_tec.group = Group.objects.get(id=request.POST['group'])
            tags = request.POST.getlist('tec_tag')
            # print('****tags', tags, new_tec.tname, new_tec.file, new_tec.status,new_tec.author, new_tec.group)
            # new_tec.created_at = timezone.now().strftime("%Y-%m-%d %H:%m:%S")
            # print(new_tec.created_at) 
            new_tec.save()
            # form.save_m2m()
            if tags:
                print('test')
                for atag in tags:
                    tag = TecTag.objects.get(tag=atag)
                    print(tag)
                    new_tec.tec_tag.add(tag)
            return redirect("asset:tec_list")     
        else:
            return HttpResponse("3")
    else:
        groups = Group.objects.all()
        tec_tags = TecTag.objects.all()
        return render(request, "asset/add_tec.html", {"groups": groups, "tec_tags": tec_tags,"form":form})

@login_required(login_url="/account/login")
def unprocess_tec_detail(request, tec_id):
    # 未处理的优秀实践详情
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        tec = get_object_or_404(TecContent, id=tec_id)
        return render(request, "asset/unprocess_pl_detail.html", {"tec":tec, "userinfo":userinfo})
    elif role.role_name == "M":
        tec = get_object_or_404(TecContent, id=tec_id)
        return render(request, "asset/unprocess_m_detail.html", {"tec":tec, "userinfo":userinfo})

@login_required(login_url="/account/login")
def processed_tec_detail(request, tec_id):
    # 已处理的优秀实践详情
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        tec = get_object_or_404(TecContent, id=tec_id)
        node = get_object_or_404(NodeMessage, name_id=tec_id)
        user = get_object_or_404(UserInfo, role_id=4)
        return render(request, "asset/processed_pl_detail.html", {"tec": tec, "userinfo": userinfo, "node": node, "user": user})
    elif role.role_name == "M":
        tec = get_object_or_404(TecContent, id=tec_id)
        node = get_object_or_404(NodeMessage, name_id=tec_id)
        return render(request, "asset/processed_m_detail.html", {"tec":tec, "userinfo":userinfo, "node":node})

@login_required(login_url="/account/login")
def download_tec_file(request, tec_id):
    # 下载优秀实践附件
    tec = get_object_or_404(TecContent, id=tec_id)
    if tec.file != "":
        file_name = tec.file.name.split('/')[1]
        response = FileResponse(tec.file)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(
            escape_uri_path(file_name))
        return response
    else:
        return HttpResponse("null")

@login_required(login_url="/account/login")
@csrf_exempt
@require_POST
def group_user(request):
    """接收处理Ajax请求"""
    
    # 前端约定的返回格式 
    result = {"rescode":'0',"message":'success',"data":[]}
    group = Group.objects.get(id=request.POST['group_id'])
    users = group.user_group.all()
    for user in users:
        user = model_to_dict(user) # model对象转换为dict字典
        result["data"].append(user)
    # json_user = serializers.serialize('json', users)
    # return HttpResponse(json_user, content_type='application/json')
    return JsonResponse(result)
