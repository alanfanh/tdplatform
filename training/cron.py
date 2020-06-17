# 定时调度任务
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from .models import Course


# 部门邮件常量
DEPARTMENT = 'xcm--1rx0thmwvgkkexzimimytgtkuqzhwlsufwjtaztwkucqgpf@tenda.cn'


def send(request):
    subject = '主题'  # 主题
    message = ''		#内容
    sender = settings.EMAIL_FROM		#发送邮箱，已经在settings.py设置，直接导入
    receiver = [email]		#目标邮箱
    html_message = '<h1>%s</h1>'%content		#发送html格式
    send_mail(subject,message,sender,receiver,html_message=html_message)

def send_course_email():
    now = datetime.now()
    courses = Course.objects.filter(course_time__gt=now)
    for c in courses:
        if c.range == "测试部":
            recipient_list = []
            subject = "部门培训通知-%s" % c.cname
            message = "培训地点：%s  培训时间：%s  培训主讲人：%s" % (c.address,c.course_time,c.teacher.realname)
            recipient_list.append(DEPARTMENT)
            send_mail(
                subject=subject, message=message, from_email='shiyanshi@tenda.cn', recipient_list=recipient_list
            )
