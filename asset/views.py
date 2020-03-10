from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Articles
from account.models import UserInfo

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
#

@login_required(login_url="/account/login")
def my_complaint(request):
    userinfo = UserInfo.objects.get(user=request.user)
    return render(request,"asset/pl_complaint_list.html",{"userinfo":userinfo})