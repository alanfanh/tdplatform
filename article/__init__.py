from django.apps import AppConfig
import os

# 修改training应用在后台管理中的名字为中文

verbose_app_name = '技术文档'

default_app_config = 'article.ArticleConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class ArticleConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = verbose_app_name
