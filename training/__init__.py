from django.apps import AppConfig
import os

# 修改training应用在后台管理中的名字为中文

verbose_app_name = '培训管理'

default_app_config = 'training.TrainingConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class TrainingConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = verbose_app_name
