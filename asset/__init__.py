from django.apps import AppConfig
import os


verbose_app_name = '技术资产'

default_app_config = 'asset.AssetConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class AssetConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = verbose_app_name
