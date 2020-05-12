# -*- coding:utf-8 -*-

from django.apps import AppConfig
import os


verbose_app_name = '账户应用'

default_app_config = 'account.AccountConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class AccountConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = verbose_app_name
