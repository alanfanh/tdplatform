import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
# Create your views here.
from .models import Articles, TecContent, Complaint, TecTag, NodeMessage, Patent, Project
from account.models import UserInfo, Role, Group

from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Q
from .forms import TecContentForm, ComplaintForm, PatentForm, ProjectForm

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
    template_view = "asset/pl_complaint_list.html"
    return render(request, template_view, {"userinfo": userinfo, "complaints_list": complaints_list})

@login_required(login_url="/account/login")
def my_complaint_data(request):
    # 返回complaint_list的json数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    userinfo = UserInfo.objects.get(user=request.user)
    complaints_list = Complaint.objects.filter(created_by=request.user)
    if request.GET.get('limit'):
        limit = int(request.GET.get('limit'))
        paginator = Paginator(complaints_list, limit)
    else:
        limit = 10
        paginator = Paginator(complaints_list, limit)
    page = request.GET.get('page')
       
    try:
        complaints_page = paginator.page(page)
        # 获取当前页面，实现当前页条目序号
        current_page = int(page)
        strat = (current_page-1)*limit
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        complaints_page = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        complaints_page = paginator.page(paginator.num_pages)
            
    for complaint in complaints_page:
        obj = model_to_dict(complaint, fields=['id','cname','type','submitter','ctime','level','product_line','category','tester','analysis_time','status'])
        # 顺序编号
        strat = strat + 1
        obj["num"] = strat
        try:
            obj['ctime'] = obj['ctime'].strftime('%Y-%m-%d')
            obj['analysis_time'] = obj['analysis_time'].strftime('%Y-%m-%d')        
        except:
            pass
        result['data'].append(obj)
    result['count'] = complaints_list.count()  
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

@login_required(login_url="/account/login")
def assigned_list(request):
    # 指派给ste、te的客诉
    userinfo = UserInfo.objects.get(user=request.user)
    complaints = Complaint.objects.filter(tester=userinfo.realname)    
    template_view = "asset/assigned_list.html"
    return render(request, template_view, {"userinfo":userinfo, "complaints":complaints})

@login_required(login_url="/account/login")
def assigned_list_data(request):
    # 指派给ste、te的客诉
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    userinfo = UserInfo.objects.get(user=request.user)
    complaints = Complaint.objects.filter(tester=userinfo.realname)
    # 每页显示10条
    if request.GET.get('limit'):
        limit = int(request.GET.get('limit'))
        paginator = Paginator(complaints, limit)
    else:
        limit = 10
        paginator = Paginator(complaints, limit)        
    page = request.GET.get('page')    
    try:
        assigned_page = paginator.page(page)    
        current_page = int(page)
        strat = (current_page-1)*limit  
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        assigned_page = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        assigned_page = paginator.page(paginator.num_pages)
    
    for assigned in assigned_page:
        obj = model_to_dict(assigned, fields=['id','cname','type','submitter','ctime','level','product_line','category','tester','analysis_time','status'])
        # 顺序编号
        strat = strat + 1
        obj["num"] = strat        
        try:
            obj['ctime'] = obj['ctime'].strftime('%Y-%m-%d')
            obj['analysis_time'] = obj['analysis_time'].strftime('%Y-%m-%d')        
        except:
            pass
        result['data'].append(obj)
    result['count'] = complaints.count()  
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

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
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(complaints, limit)
    else:
        paginator = Paginator(complaints, 10)
    page = request.GET.get('page')
    try:
        complaints_page = paginator.page(page)
    except PageNotAnInteger:
        complaints_page = paginator.page(1)
    except EmptyPage:
        complaints_page = paginator.page(paginator.num_pages)
    for complaint in complaints_page:
        obj = model_to_dict(complaint, fields=['id','cname','type','submitter','ctime','level','product_line','category','tester','status','oa_number','area','product', 'version','created_by'])
        obj['ctime'] = obj['ctime'].strftime('%Y-%m-%d')
        obj['created_by'] = get_object_or_404(UserInfo, pk=obj['created_by']).realname
        result['data'].append(obj)
    result['count'] = complaints.count()
    # print(result)
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
        if form.is_valid():
            new_complaint = form.save(commit=False)
            new_complaint.created_by = request.user
            new_complaint.save()
            return redirect("asset:complaint_list")
        else:
            error = form.errors
            # print(error)
            return render(request, 'asset/add_complaint.html', {'form': form, 'error': error})
    else:
        return render(request, "asset/add_complaint.html", {"form":form})

@login_required(login_url="/account/login")
@csrf_exempt
def edit_complaint(request, complaint_id):
    # 编辑客诉信息
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == "GET":
        form = ComplaintForm(instance=complaint)
        return render(request, "asset/edit_complaint.html", {"complaint":complaint,"form":form})
    else:
        form = ComplaintForm(request.POST, request.FILES,instance=complaint)
        upfile_name = request.FILES.get('cfile')        
        if form.is_valid() and complaint.cfile == '' and upfile_name is None:
            # 附件为空时提示上传附件
            form.add_error("cfile", u"请选择上传附件。")
            flag = 0
        elif form.is_valid() and complaint.cfile != '':
            flag = 1
        else:
            flag = 0
        
        error = form.errors
        if flag == 1:
            new_complaint = form.save(commit=False)
            new_complaint.created_by = request.user
            new_complaint.save()
            return redirect("asset:complaint_list")
        else:
            return render(request, 'asset/edit_complaint.html', {"complaint":complaint, "form":form, 'error': error})
            # return HttpResponse('1')

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
    unproc_num = ''
    if role.role_name == "PL":
        # PL用户
        tec_list = TecContent.objects.filter(status="1", group_id=userinfo.group_id)
        unproc_num = tec_list.count()
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
        # return render(request, template_view,{"userinfo":userinfo, "tec_list":tec_list,"tecs": groupnum})
        rsp = render(request, template_view,{"userinfo":userinfo, "tec_list":tec_list,"tecs": groupnum})
        rsp.set_cookie("unproc_num_cookie",unproc_num, path='/')
        return rsp

    elif role.role_name == "M":
        # M用户
        tec_list = TecContent.objects.filter(status="2")
        unproc_num = tec_list.count()
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
        # return render(request, template_view, {"userinfo": userinfo, "tec_list": tec_list, "tecs": groupnum})
        rsp = render(request, template_view, {"userinfo": userinfo, "tec_list": tec_list, "tecs": groupnum})
        rsp.set_cookie("unproc_num_cookie", unproc_num, path='/')
        return rsp
    else:
        return HttpResponse('Not Found')

@login_required(login_url="account/login")
def process_tec(request):
    # 已处理的优秀实践
    userinfo =  UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        tec_list = TecContent.objects.filter(group_id=userinfo.group_id).exclude(status="1")
        unprocess_tec_list = TecContent.objects.filter(
            status="1", group_id=userinfo.group_id)
        # 每页显示10条
        # paginator = Paginator(tec_list, 10)
        # page = request.GET.get('page')
        # try:
        #     groupnum = paginator.page(page)
        #     # 获取当前页面，实现当前页条目序号
        #     current_page = int(page)
        #     strat = (current_page-1)*10
        # except PageNotAnInteger:
        #     # 如果请求的页数不是整数, 返回第一页。
        #     groupnum = paginator.page(1)
        # except EmptyPage:
        #     # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        #     groupnum = paginator.page(paginator.num_pages)
        template_view = "asset/processed_pl.html"
        return render(request, template_view, {"userinfo": userinfo, "tec_list": tec_list, "tecs": unprocess_tec_list})
    elif role.role_name == "M":
        tec_list = TecContent.objects.exclude(status="2")
        tec_list = tec_list.exclude(status="1")
        unprocess_tecs = TecContent.objects.filter(status="2")
        # 每页显示10条
        # paginator = Paginator(tec_list, 10)
        # page = request.GET.get('page')
        # try:
        #     groupnum = paginator.page(page)
        #     # 获取当前页面，实现当前页条目序号
        #     current_page = int(page)
        #     strat = (current_page-1)*10
        # except PageNotAnInteger:
        #     # 如果请求的页数不是整数, 返回第一页。
        #     groupnum = paginator.page(1)
        # except EmptyPage:
        #     # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        #     groupnum = paginator.page(paginator.num_pages)
        template_view = "asset/processed_m.html"
        return render(request, template_view, {"userinfo": userinfo, "tec_list": tec_list, "tecs": unprocess_tecs})
    else:
        return HttpResponse("Not Found")

@login_required(login_url="")
def process_tec_data(request):
    # 已处理的优秀实践，分PL和M用户
    result = {"code":0, "msg":"", "count": 100, "data":[]}
    kv = {"0": "驳回", "1": "审核中", "2": "审核中", "3": "完成"}
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        tecs = TecContent.objects.filter(group_id=userinfo.group_id).exclude(status="1")
    elif role.role_name == "M":
        tecs = TecContent.objects.exclude(status="2")
        tecs = tecs.exclude(status="1")
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(tecs, limit)
    else:
        paginator = Paginator(tecs, 10)
    page = request.GET.get('page')
    try:
        tecs_page = paginator.page(page)
    except PageNotAnInteger:
        tecs_page = paginator.page(1)
    except EmptyPage:
        tecs_page = paginator.page(paginator.num_pages)
    for tec in tecs_page:
        obj = model_to_dict(tec, exclude=['file', ])
        obj['created_at'] = tec.created_at.strftime('%Y-%m-%d')
        tag_list = []
        for tag in tec.tec_tag.all():
            tag_list.append(tag.tag)
        obj['tec_tag'] = tag_list
        obj['group'] = Group.objects.get(id=obj['group']).name
        obj['author'] = UserInfo.objects.get(id=obj['author']).realname
        obj['status'] = kv[obj['status']]
        result['data'].append(obj)
    result['count'] = tecs.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii":False})

@login_required(login_url="/account/login")
def my_tec(request):
    # STE添加的优秀实践, 页面路由
    userinfo = UserInfo.objects.get(user=request.user)
    # ste_tecs = TecContent.objects.filter(author=userinfo)
    ste_tecs = TecContent.objects.filter(status="3", author=userinfo)
    template_view = "asset/my_tec.html"
    return render(request, template_view, {"userinfo": userinfo, "ste_tecs": ste_tecs})

@login_required(login_url="/account/login")
def my_tec_data(request):
    # 个人申请优秀实践，返回json格式的数据
    result = {"code":0, "msg":"", "count": 1000, "data": []}
    kv = {"0":"驳回","1":"审核中", "2":"审核中","3":"完成"}
    userinfo = UserInfo.objects.get(user=request.user)
    # 筛选自己提交的实践
    tecs = TecContent.objects.filter(author=userinfo)
    # 获取url附带的参数，进行分页处理
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(tecs, limit)
    else:
        paginator = Paginator(tecs, 10)
    page = request.GET.get('page')
    try:
        tecs_page = paginator.page(page)
    except PageNotAnInteger:
        tecs_page = paginator.page(1)
    except EmptyPage:
        tecs_page = paginator.page(paginator.num_pages)
    for tec in tecs_page:
        obj = model_to_dict(tec, exclude=['file',])
        obj['created_at'] = tec.created_at.strftime('%Y-%m-%d')
        tag_list = []
        for tag in tec.tec_tag.all():
            tag_list.append(tag.tag)
        obj['tec_tag'] = tag_list
        obj['group'] = Group.objects.get(id=obj['group']).name
        obj['author'] = UserInfo.objects.get(id=obj['author']).realname
        obj['status'] = kv[obj['status']]
        result['data'].append(obj)
    result['count'] = tecs.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii":False})

@login_required(login_url="/account/login")
@csrf_exempt
def filter_status_myteclist(request):
    # ajax请求，筛选不同状态数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    # 筛选请求用户的数据记录
    userinfo = UserInfo.objects.get(user=request.user)
    ste_tecs = TecContent.objects.filter(author=userinfo)    
    if request.GET.get('range_name'):
        # 过滤状态        
        status_id = request.GET.get('range_name')        
        if status_id == "进行中":
            ste_tecs = ste_tecs.filter(Q(status='1') | Q(status='2'))
        else:                       
            ste_tecs = ste_tecs.filter(status=status_id)

    # 每页显示10条
    if request.GET.get('limit'):
        limit = int(request.GET.get('limit'))
        paginator = Paginator(ste_tecs, limit)
    else:
        limit = 10
        paginator = Paginator(ste_tecs, limit)

    # 获取前台传入后台的page值
    page = request.GET.get('page')
    try:
        cur_tecs = paginator.page(page)    
        current_page = int(page)
        strat = (current_page-1)*limit  
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        cur_tecs = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        cur_tecs = paginator.page(paginator.num_pages)

    for cur_tec in cur_tecs:
        obj = model_to_dict(cur_tec, fields=['id','tname','author','group','tec_tag','created_at','status'])
        obj["created_at"] = cur_tec.created_at.strftime('%Y-%m-%d')
        # 获取tec标签，多对多查询
        tag_list = [tag.tag for tag in cur_tec.tec_tag.all()]
        obj['tec_tag'] = tag_list
        obj['group'] = Group.objects.get(id=obj['group']).name
        obj['author'] = UserInfo.objects.get(id=obj['author']).realname
        # 顺序编号
        strat = strat + 1
        obj["num"] = strat     
        result['data'].append(obj)
    result['count'] = ste_tecs.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

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
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(tecs, limit)
    else:
        paginator = Paginator(tecs, 10)
    page = request.GET.get('page')
    try:
        tecs_page = paginator.page(page)
        # 获取当前页面，生成页面条目序号
        current_page = int(page)
    except PageNotAnInteger:
        tecs_page = paginator.page(1)
    except EmptyPage:
        tecs_page = paginator.page(paginator.num_pages)
    for tec in tecs_page:
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
    # print(result)
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
                # print('test')
                for atag in tags:
                    tag = TecTag.objects.get(tag=atag)
                    # print(tag)
                    new_tec.tec_tag.add(tag)
            # return redirect("asset:tec_list")
            role = Role.objects.get(role_name="PL")
            userinfo = UserInfo.objects.filter(group=new_tec.group,role=role)
            return render(request, "asset/add_success.html", {"newtec":new_tec})
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
        node = get_object_or_404(NodeMessage, name=tec)
        return render(request, "asset/unprocess_m_detail.html", {"tec":tec, "userinfo":userinfo,"node":node})

@login_required(login_url="/account/login")
def processed_tec_detail(request, tec_id):
    # 已处理的优秀实践详情
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    if role.role_name == "PL":
        # get_object_or_404必须返回唯一对象，最好传入主键
        tec = get_object_or_404(TecContent, id=tec_id)
        node = get_object_or_404(NodeMessage, name_id=tec_id)
        # user = get_object_or_404(UserInfo, role_id=4)
        return render(request, "asset/processed_pl_detail.html", {"tec": tec, "userinfo": userinfo, "node": node})
    elif role.role_name == "M":
        tec = get_object_or_404(TecContent, id=tec_id)
        node = get_object_or_404(NodeMessage, name_id=tec_id)
        return render(request, "asset/processed_m_detail.html", {"tec":tec, "userinfo":userinfo, "node":node})

@login_required(login_url="/account/login")
def my_process_tec(request, tec_id):
    # te和ste所提交优秀实践
    userinfo = UserInfo.objects.get(user=request.user)
    tec = get_object_or_404(TecContent, pk=tec_id)
    ste_tecs = TecContent.objects.filter(author=userinfo, status="3")
    if tec.status == "1":
        return render(request, "asset/te/unprocess_tec.html", {"tec": tec, "userinfo": userinfo, "ste_tecs": ste_tecs})
    elif tec.status == "2":
        node = get_object_or_404(NodeMessage, name_id=tec_id)
        return render(request, "asset/te/process_tec.html", {"tec":tec, "userinfo":userinfo, "node":node, "ste_tecs":ste_tecs})
    elif tec.status == "3":
        node = get_object_or_404(NodeMessage, name_id=tec_id)
        return render(request, "asset/te/complete_tec.html", {"tec": tec, "userinfo": userinfo, "node": node, "ste_tecs": ste_tecs})

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
        if year != "All":
            tecs = tecs.filter(created_at__year=year)
    if request.GET.get('tag_id'):
        # 筛选tec标签
        tag_id = request.GET.get('tag_id')
        tecs = tecs.filter(tec_tag=tag_id)
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(tecs, limit)
    else:
        paginator = Paginator(tecs, 10)
    page = request.GET.get('page')
    try:
        tecs_page = paginator.page(page)
        # 获取当前页面，生成页面条目序号
        current_page = int(page)
    except PageNotAnInteger:
        tecs_page = paginator.page(1)
    except EmptyPage:
        tecs_page = paginator.page(paginator.num_pages)
    for tec in tecs_page:
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
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(complaints, limit)
    else:
        paginator = Paginator(complaints, 10)
    page = request.GET.get('page')
    try:
        coms_page = paginator.page(page)
        # 获取当前页面，生成页面条目序号
        current_page = int(page)
    except PageNotAnInteger:
        coms_page = paginator.page(1)
    except EmptyPage:
        coms_page = paginator.page(paginator.num_pages)
    for com in coms_page:
        obj = model_to_dict(com, fields=['id','cname','type','submitter','ctime','level','product_line','category','tester','status'])
        obj['ctime'] = obj['ctime'].strftime('%Y-%m-%d')
        result['data'].append(obj)
    result['count'] = complaints.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})


# 搜索框搜索数据并返回

@login_required(login_url="/account/login")
@csrf_exempt
def search_tec(request):
    # 返回json数据
    result = {"code":0, "msg":"", "count":0, "data":[]}
    # 获取数据
    if request.GET.get("search"):
        search_key = request.GET.get("search")
        tecs = TecContent.objects.filter(status="3")
        # author为外键，需author__realname关联UserInfo的实际姓名
        tecs = tecs.filter(Q(tname__icontains=search_key)|Q(author__realname__icontains=search_key))
        for tec in tecs:
            obj=model_to_dict(tec, exclude=['file', ])
            obj["created_at"] = tec.created_at.strftime('%Y-%m-%d')
            tag_list = []
            for tag in tec.tec_tag.all():
                tag_list.append(tag.tag)
            obj['tec_tag'] = tag_list
            obj['group'] = Group.objects.get(id=obj['group']).name
            obj['author'] = UserInfo.objects.get(id=obj['author']).realname
            result['data'].append(obj)
        result['count'] = tecs.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii":False})

@login_required(login_url="/account/login")
@csrf_exempt
def search_complaint(request):
    # 根据搜索关键字，返回json数据
    result = {"code":0, "msg":"", "count":0, "data":[]}
    # 获取数据
    if request.GET.get("search"):
        search_key = request.GET.get("search")
        # 模糊匹配标题、提交人、分析责任人
        complaints = Complaint.objects.filter(
            Q(cname__icontains=search_key) | Q(submitter__icontains=search_key) | Q(tester__icontains=search_key))
        for com in complaints:
            obj = model_to_dict(com, fields=['id','cname','type','submitter','ctime','level','product_line','category','tester','status'])
            obj['ctime'] = obj['ctime'].strftime('%Y-%m-%d')
            result['data'].append(obj)
        result['count'] = complaints.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii':False})


@login_required(login_url="/account/login")
@csrf_exempt
@require_POST
def check_tec(request):
    # 审核优秀实践
    tec_id = request.POST.get('tec_id')
    option = request.POST.get('option')
    note = request.POST.get('note') 
    userinfo = UserInfo.objects.get(user=request.user)
    if userinfo.role.role_name == "PL":
        # 组长审核信息
        tec = TecContent.objects.get(id=tec_id)
        new_node = NodeMessage.objects.filter(name=tec)
        if new_node.exists():
            new_node = new_node[0]
        else:
            new_node = NodeMessage(name=tec)
        new_node.pl_name = userinfo.realname
        new_node.pl_decide = option
        if option == "同意":
            tec.status = 2
        else:
            tec.status = 0
        new_node.pl_notes = note
        new_node.pl_time = datetime.datetime.now()
        new_node.m_time = datetime.datetime.now()
        new_node.save()
        tec.save()
        print(tec_id,option,note)
        return HttpResponse("1")
    elif userinfo.role.role_name == "M":
        tec = TecContent.objects.get(id=tec_id)
        m = NodeMessage.objects.get(name=tec)
        m.m_name = userinfo.realname
        m.m_decide = option
        if option == "同意":
            tec.status = 3
        else:
            tec.status = 0
        m.m_notes = note
        m.m_time = datetime.datetime.now()
        m.save()
        tec.save()
        return HttpResponse("1")
    else:
        return HttpResponse('404')

# 筛选状态
@login_required(login_url="/account/login")
def filter_tec_status(request):
    result = {"code":0, "msg":"", "count":0, "data":[]}
    kv = {"0": "驳回", "1": "审核中", "2": "审核中", "3": "完成"}
    userinfo = UserInfo.objects.get(user=request.user)
    role = Role.objects.get(id=userinfo.role_id)
    # 判断当前用户角色，返回不同数据
    if role.role_name == "PL":
        tecs = TecContent.objects.filter(group_id=userinfo.group_id).exclude(status="1")
    elif role.role_name == "M":
        tecs = TecContent.objects.exclude(Q(status="2") | Q(status="1"))
    else:
        tecs = TecContent.objects.filter(author=userinfo)
    if request.GET.get('status'):
        status = request.GET.get('status')
        if status == "1&2":
            status = status.split('&')
            tecs = tecs.filter(Q(status=status[0]) | Q(status=status[1]))
        else:
            tecs = tecs.filter(status=status)
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(tecs, limit)
    else:
        paginator = Paginator(tecs, 10)
    page = request.GET.get('page')
    try:
        tecs_page = paginator.page(page)
    except PageNotAnInteger:
        tecs_page = paginator.page(1)
    except EmptyPage:
        tecs_page = paginator.page(paginator.num_pages)
    for tec in tecs_page:
        obj = model_to_dict(tec, exclude=['file', ])
        obj['created_at'] = tec.created_at.strftime('%Y-%m-%d')
        tag_list = []
        for tag in tec.tec_tag.all():
            tag_list.append(tag.tag)
        obj['tec_tag'] = tag_list
        obj['group'] = Group.objects.get(id=obj['group']).name
        obj['author'] = UserInfo.objects.get(id=obj['author']).realname
        obj['status'] = kv[obj['status']]
        result['data'].append(obj)
    # 统计总数，用于前端分页
    result['count'] = tecs.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii":False})


@login_required(login_url="/account/login")
def patent_list(request):
    template_view = "asset/patent/patent_list.html"
    return render(request, template_view)


@login_required(login_url="/account/login")
def patent_list_data(request):
    # 返回json数据
    result_data = {"code":0, "msg":"", "count":0, "data":[]}
    patents = Patent.objects.all()
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(patents, limit)
    else:
        paginator = Paginator(patents, 10)
    page = request.GET.get('page')
    try:
        patents_page = paginator.page(page)
    except PageNotAnInteger:
        patents_page = paginator.page(1)
    except EmptyPage:
        patents_page = paginator.page(paginator.num_pages)
    for patent in patents_page:
        obj = model_to_dict(patent, fields=['id','name','type','author','group','submit_time','created_at','status','patent_id','award'])
        obj['submit_time'] = obj['submit_time'].strftime('%Y-%m-%d')
        obj['author'] = get_object_or_404(UserInfo, pk=obj['author']).realname
        obj['group'] = get_object_or_404(Group, pk=obj['group']).name
        result_data['data'].append(obj)
    result_data['count'] = patents.count()
    return JsonResponse(result_data, json_dumps_params={'ensure_ascii': False})


@login_required(login_url="/account/login")
@csrf_exempt
def add_patent(request):
    # 添加优秀实践
    form = PatentForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            new_patent = form.save(commit=False)
            # new_tec.author = UserInfo.objects.get(id=request.POST['author'])
            # new_tec.group = Group.objects.get(id=request.POST['group'])
            # tags = request.POST.getlist('tec_tag')
            # new_tec.created_at = timezone.now().strftime("%Y-%m-%d %H:%m:%S")
            # print(new_tec.created_at)
            new_patent.save()
            # form.save_m2m()
            return redirect("asset:patent_list")
            # role = Role.objects.get(role_name="PL")
            # userinfo = UserInfo.objects.filter(group=new_patent.group,role=role)
            # return render(request, "asset/add_success.html", {"newtec":new_patent})
        else:
            error = form.errors
            groups = Group.objects.all()
            print(error)
            return render(request, 'asset/patent/add_patent.html', {'form': form, 'error': error, "groups":groups})
    else:
        groups = Group.objects.all()
        return render(request, "asset/patent/add_patent.html", {"groups": groups, "form":form})

@login_required(login_url="/account/login")
def download_patent_file(request, patent_id):
    # 下载优秀实践附件
    patent = get_object_or_404(Patent, id=patent_id)
    if patent.file != "":
        file_name = patent.file.name.split('/')[1]
        response = FileResponse(patent.file)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(
            escape_uri_path(file_name))
        return response
    else:
        return HttpResponse("null")


@login_required(login_url="/account/login")
def filter_patent_range(request):
    # ajax请求，筛选不同部门范围的数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    # 筛选出所有的数据记录
    patents = Patent.objects.all()
    if request.GET.get('range_name'):
        # 过滤部门范围
        range_id = request.GET.get('range_name')
        patents = patents.filter(group_id=range_id)
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(patents, limit)
    else:
        paginator = Paginator(patents, 10)
    page = request.GET.get('page')
    try:
        patents_page = paginator.page(page)
        # 获取当前页面，生成页面条目序号
        current_page = int(page)
    except PageNotAnInteger:
        patents_page = paginator.page(1)
    except EmptyPage:
        patents_page = paginator.page(paginator.num_pages)
    for tec in patents_page:
        obj = model_to_dict(tec, exclude=['file', ])
        obj["submit_time"] = tec.created_at.strftime('%Y-%m-%d')
        obj['group'] = Group.objects.get(id=obj['group']).name
        obj['author'] = UserInfo.objects.get(id=obj['author']).realname
        result['data'].append(obj)
    result['count'] = patents.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

@login_required(login_url="/account/login")
def search_patent(request):
    # 返回json数据
    result = {"code": 0, "msg": "", "count": 0, "data": []}
    # 获取数据
    if request.GET.get("search"):
        search_key = request.GET.get("search")
        tecs = TecContent.objects.filter(status="3")
        # author为外键，需author__realname关联UserInfo的实际姓名
        patents = Patent.objects.filter(Q(name__icontains=search_key) |
                           Q(author__realname__icontains=search_key))
        for patent in patents:
            obj = model_to_dict(patent, exclude=['file', ])
            obj["submit_time"] = patent.created_at.strftime('%Y-%m-%d')
            obj['group'] = Group.objects.get(id=obj['group']).name
            obj['author'] = UserInfo.objects.get(id=obj['author']).realname
            result['data'].append(obj)
        result['count'] = tecs.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii": False})

@login_required(login_url="/account/login")
@csrf_exempt
def edit_patent(request, patent_id):
    # 编辑客诉信息
    patent = Patent.objects.get(id=patent_id)
    if request.method == "GET":
        form = PatentForm(instance=patent)
        groups = Group.objects.all()
        return render(request, "asset/patent/edit_patent.html", {"patent": patent, "form": form, "groups":groups})
    else:
        form = PatentForm(request.POST, request.FILES, instance=patent)
        upfile_name = request.FILES.get('file')
        if form.is_valid() and patent.file == '' and upfile_name is None:
            # 附件为空时提示上传附件
            form.add_error("cfile", u"请选择上传附件。")
            flag = 0
        elif form.is_valid() and patent.file != '':
            flag = 1
        else:
            flag = 0

        error = form.errors
        if flag == 1:
            new_patent = form.save(commit=False)
            new_patent.save()
            return redirect("asset:patent_list")
        else:
            return render(request, 'asset/patent/edit_patent.html', {"patent": patent, "form": form, 'error': error})


# 企业网BU项目过程质量数据
@login_required(login_url="/account/login")
def project_list(request):
    template_view = "asset/project/project_list.html"
    return render(request, template_view)

@login_required(login_url="/account/login")
def project_list_data(request):
    result_data = {"code": 0, "msg": "", "count": 0, "data": []}
    projects = Project.objects.all()
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(projects, limit)
    else:
        paginator = Paginator(projects, 10)
    page = request.GET.get('page')
    try:
        projects_page = paginator.page(page)
    except PageNotAnInteger:
        projects_page = paginator.page(1)
    except EmptyPage:
        projects_page = paginator.page(paginator.num_pages)
    for project in projects_page:
        obj = model_to_dict(project, fields=[
                            'id', 'name', 'type', 'created_at', 'completed_time', 'coder', 'developer', 'tester', 'changed','newbug_percent', 'reopen_count', 'missing_percent', 'nocase_found', 'test_round', 'reject_count', 'reject_reason', 'deliver','delay', 'delay_percent','delay_reason','day_round','per_version','perf_count','beta_bug','customer_bug','quality_issue','solution','cost_percent','pcb_count','item_percent','tec_count','tec','note'])
        if obj['completed_time'] != None:
            obj['completed_time'] = obj['completed_time'].strftime('%Y-%m-%d')
        if obj['deliver'] != None:
            obj['deliver'] = obj['deliver'].strftime('%Y-%m-%d')
        obj['created_at'] = obj['created_at'].strftime('%Y-%m-%d')
        result_data['data'].append(obj)
    result_data['count'] = projects.count()
    return JsonResponse(result_data, json_dumps_params={'ensure_ascii':False})


@login_required(login_url="/account/login")
@csrf_exempt
def add_project(request):
    # 添加项目数据
    form = ProjectForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.save()
            return redirect("asset:project_list")
        else:
            error = form.errors
            return render(request, "asset/project/add_project.html",{"form":form, "error":error})
    else:
        return render(request, "asset/project/add_project.html",{"form":form})


@login_required(login_url="/account/login")
@csrf_exempt
def edit_project(request,project_id):
    # 编辑项目数据
    project = Project.objects.get(id=project_id)
    if request.method == "GET":
        form = ProjectForm(instance=project)
        return render(request, "asset/project/edit_project.html", {"project": project, "form": form})
    else:
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.save()
            return redirect("asset:project_list")
        else:
            error = form.errors
            return render(request, 'asset/project/edit_project.html', {"project":project, "form":form, 'error': error})
            # return HttpResponse('1')


@login_required(login_url="/account/login")
@csrf_exempt
def project_detail(request,project_id):
    # 项目详细信息
    project = Project.objects.get(id=project_id)
    return render(request, 'asset/project/project_detail.html', {"project":project})

@login_required(login_url="/account/login")
def filter_project_type(request):
    # ajax请求，筛选不同项目类型的数据
    result = {"code": 0, "msg": "", "count": 1000, "data": []}
    # 筛选出所有的数据记录
    projects = Project.objects.all()
    if request.GET.get('type_name'):
        # 过滤项目类型
        type_name = request.GET.get('type_name')
        projects = projects.filter(type=type_name)
    if request.GET.get('limit'):
        limit = request.GET.get('limit')
        paginator = Paginator(projects, limit)
    else:
        paginator = Paginator(projects, 10)
    page = request.GET.get('page')
    try:
        projects_page = paginator.page(page)
        # 获取当前页面，生成页面条目序号
        current_page = int(page)
    except PageNotAnInteger:
        projects_page = paginator.page(1)
    except EmptyPage:
        projects_page = paginator.page(paginator.num_pages)
    for project in projects_page:
        obj = model_to_dict(project, exclude=['file', ])
        if obj['completed_time'] != None:
            obj['completed_time'] = obj['completed_time'].strftime(
                    '%Y-%m-%d')
        if obj['deliver'] != None:
            obj['deliver'] = obj['deliver'].strftime('%Y-%m-%d')
        obj['created_at'] = obj['created_at'].strftime('%Y-%m-%d')
        result['data'].append(obj)
    result['count'] = projects.count()
    return JsonResponse(result, json_dumps_params={'ensure_ascii': False})

@login_required(login_url="/account/login")
def search_project(request):
    # 返回json数据
    result = {"code": 0, "msg": "", "count": 0, "data": []}
    # 获取数据,项目名称
    if request.GET.get("search"):
        search_key = request.GET.get("search")
        tecs = TecContent.objects.filter(status="3")
        # 过滤project项目名
        projects = Project.objects.filter(Q(name__icontains=search_key))
        for p in projects:
            obj = model_to_dict(p, exclude=['file', ])
            if obj['completed_time'] != None:
                obj['completed_time'] = obj['completed_time'].strftime('%Y-%m-%d')
            if obj['deliver'] != None:
                obj['deliver'] = obj['deliver'].strftime('%Y-%m-%d')
            obj['created_at'] = obj['created_at'].strftime('%Y-%m-%d')
            result['data'].append(obj)
        result['count'] = tecs.count()
    return JsonResponse(result, json_dumps_params={"ensure_ascii": False})
