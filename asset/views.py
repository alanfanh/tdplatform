from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
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
    complaints_list = Complaint.objects.filter(created_by=request.user)
    # 每页显示10条
    paginator = Paginator(complaints_list, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            complaints = paginator.page(page)
            # 获取当前页面，实现当前页条目序号
            current_page = int(page)
            strat = (current_page-1)*10
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            complaints = paginator.page(1)
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            complaints = paginator.page(paginator.num_pages)
    template_view = "asset/pl_complaint_list.html"
    return render(request, template_view, {"userinfo": userinfo, "complaints": complaints, "complaints_list": complaints_list})

@login_required(login_url="/account/login")
def assigned_list(request):
    # 指派给ste、te的客诉
    userinfo = UserInfo.objects.get(user=request.user)
    complaints = Complaint.objects.filter(tester=userinfo.realname)
    #每页显示10条
    paginator = Paginator(complaints, 10)
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
    template_view = "asset/assigned_list.html"
    return render(request, template_view, {"userinfo":userinfo, "complaints":complaints,"groupnum": groupnum})

@login_required(login_url="/account/login")
def complaint_list(request):
    complaints = Complaint.objects.all()
    userinfo = UserInfo.objects.get(user=request.user)
    return render(request, "asset/complaint_list.html", {"complaints":complaints,"userinfo":userinfo})

@login_required(login_url="/account/login")
def complaint_list_data(request):
    # 返回complaint_list的json数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    complaints = Complaint.objects.all()
    for complaint in complaints:
        obj = model_to_dict(complaint, fields=['id','cname','type','submitter','ctime','level','product_line','category','tester','status'])
        obj['ctime'] = obj['ctime'].strftime('%Y-%m-%d')
        result['data'].append(obj)
    result['count'] = complaints.count()
    print(result)
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

@login_required(login_url="/account/login")
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint,id=complaint_id)
    return render(request, "asset/complaint_detail.html", {"complaint":complaint})

@login_required(login_url="/account/login")
def download_cfile(request, complaint_id):
    # 下载客诉附件
    com = get_object_or_404(Complaint, id=complaint_id)
    if com.cfile != "":
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

@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def delete_complaint(request):
    # 删除客诉信息
    complaint_id = request.POST['complaint_id']
    userinfo = UserInfo.objects.get(user=request.user)
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.delete()
    except:
        return HttpResponse('2')


# 优秀实践

@login_required(login_url="/account/login")
def unprocess_tec(request):
    # 未处理的优秀实践
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        # PL用户
        tec_list = TecContent.objects.filter(status="1", group_id=userinfo.group_id)
        #每页显示10条
        paginator = Paginator(tec_list, 10)
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
        template_view = "asset/unprocess_pl.html"
        return render(request, template_view,{"userinfo":userinfo, "tec_list":tec_list,"groupnum": groupnum})
    elif role.role_name == "M":
        # M用户
        tec_list = TecContent.objects.filter(status="2")
        #每页显示10条
        paginator = Paginator(tec_list, 10)
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
        template_view = "asset/unprocess_m.html"
        return render(request, template_view, {"userinfo":userinfo,"tec_list":tec_list,"groupnum": groupnum})
    else:
        return HttpResponse('Not Found')

@login_required(login_url="account/login")
def process_tec(request):
    # 已处理的优秀实践
    userinfo =  UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        tec_list = TecContent.objects.filter(group_id=userinfo.group_id).exclude(status="1")
        #每页显示10条
        paginator = Paginator(tec_list, 10)
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
        template_view = "asset/processed_pl.html"
        return render(request, template_view,{"userinfo":userinfo, "tec_list":tec_list,"groupnum": groupnum})
    elif role.role_name == "M":
        tec_list = TecContent.objects.exclude(status="2")
        #每页显示10条
        paginator = Paginator(tec_list, 10)
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
        template_view = "asset/processed_m.html"
        return render(request, template_view, {"userinfo":userinfo, "tec_list":tec_list,"groupnum": groupnum})
    else:
        return HttpResponse("Not Found")

@login_required(login_url="/account/login")
def my_tec(request):
    # STE添加的优秀实践
    userinfo = UserInfo.objects.get(user=request.user)
    ste_tecs = TecContent.objects.filter(status="3")
    #每页显示10条
    paginator = Paginator(ste_tecs, 10)
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
    template_view = "asset/my_tec.html"
    return render(request, template_view, {"userinfo":userinfo,"ste_tecs":ste_tecs,"groupnum": groupnum})

@login_required(login_url="/account/login")
def tec_list(request):
    # 主页优秀实践列表
    userinfo = UserInfo.objects.get(user=request.user)
    tecs = TecContent.objects.filter(status="3")
    return render(request, "asset/tec_list.html", {"tecs":tecs,"userinfo":userinfo})

@login_required(login_url="/account/login")
def tec_list_data(request):
    # 返回tec_list的json数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    tecs = TecContent.objects.filter(status="3")
    for tec in tecs:
        obj = model_to_dict(tec, exclude=['file',])
        obj["created_at"] = tec.created_at.strftime('%Y-%m-%d')
        # 获取tec标签，多对多查询
        tag_list=[]
        for tag in tec.tec_tag.all():
            tag_list.append(tag.tag)
        obj['tec_tag'] = tag_list
        obj['group'] = Group.objects.get(id=obj['group']).name
        obj['author'] = UserInfo.objects.get(id=obj['author']).realname
        result['data'].append(obj)
    result['count'] = tecs.count()
    print(result)
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

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
def delete_tec(request):
    tec_id = request.POST['tec_id']
    try:
        tec = TecContent.objects.get(id=tec_id)
        tec.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('2')

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

@login_required(login_url="/account/login")
@csrf_exempt
def filter_tec_range(request):
    # ajax请求，筛选不同部门范围的数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    # 筛选出所有的数据记录
    tecs = TecContent.objects.filter(status="3")
    if request.GET.get('range_name'):
        # 过滤部门范围
        range_id = request.GET.get('range_name')
        tecs = tecs.filter(group_id=range_id)
    if request.GET.get('time_year'):
        # 筛选创建年
        year = request.GET.get('time_year')
        tecs = tecs.filter(created_at__year=year)
    if request.GET.get('tag_id'):
        # 筛选tec标签
        tag_id = request.GET.get('tag_id')
        tecs = tecs.filter(tec_tag=tag_id)
    for tec in tecs:
        obj = model_to_dict(tec, exclude=['file', ])
        obj["created_at"] = tec.created_at.strftime('%Y-%m-%d')
        # 获取tec标签，多对多查询
        tag_list = []
        for tag in tec.tec_tag.all():
            tag_list.append(tag.tag)
        obj['tec_tag'] = tag_list
        obj['group'] = Group.objects.get(id=obj['group']).name
        obj['author'] = UserInfo.objects.get(id=obj['author']).realname
        result['data'].append(obj)
    result['count'] = tecs.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


@login_required(login_url="/account/login")
@csrf_exempt
def filter_complaint_list(request):
    # 返回json数据
    result = {"code":0,"msg":"", "count":1000, "data":[]}
    # 获取所有数据
    complaints = Complaint.objects.all()
    if request.GET.get("product_line"):
        product = request.GET.get("product_line")
        complaints = complaints.filter(product_line=product)
    if request.GET.get("year"):
        year = request.GET.get("year")
        complaints = complaints.filter(created_at__year=year)
    if request.GET.get("type"):
        type = request.GET.get("type")
        complaints = complaints.filter(category=type)
    for com in complaints:
        obj = model_to_dict(com, fields=['id','cname','type','submitter','ctime','level','product_line','category','tester','status'])
        obj['ctime'] = obj['ctime'].strftime('%Y-%m-%d')
        result['data'].append(obj)
    result['count'] = complaints.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


# 搜索数据
@login_required(login_url="/account/login")
@csrf_exempt
def search_complaint(request):
    pass