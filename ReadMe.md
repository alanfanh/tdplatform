# tdplatform

> tdplatform is a Django Web project.

## 介绍

基于Django框架开发的td-platform，用于部门内部的交流学习、客诉管理、培训管理以及部门内部技术资产建设。

### Developer

[FanHao](http://alanfanh.github)

## 环境

### 语言

```text
python3.14 64bit
```

### 依赖

> 本地预装uv包管理器

同步项目包依赖，uv将自动把包安装项目根目录下venv虚环境中
````sh
uv sync
````
运行项目
````sh
uv run python manage.py runserver
````

### 数据库

> MySQL或者MariaDB等关系型数据库

根据models.py生成数据库迁移文件
````sh
uv run python manage.py makemigrations
````
根据迁移文件，执行操作修改数据库表
````sh
uv run python manage.py migrate
````
创建后台超级用户
````sh
uv run python manage.py createsuperuser
````

## 项目结构

> 持续更新中.....

```text
tdplatform
├── mysite                            # 项目设置目录。
│   ├── __init__.py
│   ├── settings.py                   # 项目设置。
│   ├── urls.py                       # 项目url。
│   └── wsgi.py                       # 
├── account                           # account应用
│   ├── migrations                    # 目录。数据库迁移过程中产生的文件。
│   ├── __init__.py  
│   ├── urls.py                       # url配置
│   ├── models.py                     # 数据模型
│   ├── views.py                      # 应用视图函数
│   ├── admin.py                      # 
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
├── pyproject.toml                    # uv管理器生成的项目依赖
├── uv.lock                           # uv解析所有依赖包
└── manage.py                         # django项目入口文件
```
