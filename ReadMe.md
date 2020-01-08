# tdplatform

> tdplatform is a Django Web project.

## 介绍

基于Django框架开发的td-platform，用于部门内部的交流学习、客诉管理、培训管理以及部门内部技术资产建设。

### Developer

[FanHao](http://alanfanh.github)

## 环境

### 语言

```text
python3.6 64bit
```

### 依赖

> 可使用"pip install -r requirements.txt"一键安装所有依赖项

````text
django=2.2.8
django-password-reset=2.0
pymysql=0.9.3
````

### 数据库

> MySQL或者MariaDB等关系型数据库

## 项目结构

> 持续更新中.....

```text
tdplatform
├── mysite                            # 项目设置目录。
│   ├── __init__.py
│   ├── settings.py                   # 项目设置。
│   ├── urls.py                       # 项目url。
│   └── wsgi.py                       # Android 终端范例代码。
├── account                           # 前端 npm 包。
│   ├── migrations                    # 目录。数据库迁移过程中产生的文件。
│   ├── __init__.py  
│   ├── urls.py                       # url配置
│   ├── models.py                     # 数据模型
│   ├── views.py                      # 应用视图函数
│   ├── admin.py                      # hippy-vue 中浏览器中所没有的，额外的，终端定制组件。
│   ├── forms.py                      # 表单
│   └── apps.py                       # 应用配置
├── training                          # training应用
│   ├── ...                           # 省略。结构与account应用一致。
│   └── apps.py
├── asset                             # asset应用
│   ├── ...                           # 省略
│   └── apps.py
├── media                             # 媒体文件目录
├── static                            # 项目静态文件目录。
│   ├── css                           # css文件目录
│   ├── js                            # js文件目录
│   └── ...                           # 省略
├── templates                         # 项目前端模版。
│   ├── account                       # account应用的前端模版
│   ├── ...                           # 省略其他应用
│   ├── base.html
│   ├── footer.html
│   └── header.html
├── requirements.txt                  # 项目依赖
└── manage.py                         # django项目管理文件
```
