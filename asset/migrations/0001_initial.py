# Generated by Django 2.2.10 on 2020-03-31 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_auto_20200304_1345'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=30, verbose_name='客诉名称')),
                ('type', models.CharField(max_length=10, verbose_name='客诉类型')),
                ('submitter', models.CharField(max_length=50, verbose_name='提交人')),
                ('ctime', models.DateTimeField(verbose_name='客诉时间')),
                ('product', models.CharField(max_length=10, verbose_name='产品型号')),
                ('version', models.CharField(max_length=10, verbose_name='软件版本')),
                ('level', models.CharField(choices=[('high', '高'), ('mid', '中'), ('low', '低')], max_length=50, verbose_name='严重程度')),
                ('product_line', models.CharField(max_length=20, verbose_name='产品线')),
                ('category', models.CharField(max_length=10, verbose_name='问题分类')),
                ('tester', models.CharField(max_length=10, verbose_name='分析责任人')),
                ('complete_time', models.DateTimeField(verbose_name='分析完成时间')),
                ('status', models.CharField(max_length=50, verbose_name='措施状态')),
                ('cfile', models.FileField(upload_to=None, verbose_name='材料附件')),
            ],
        ),
        migrations.CreateModel(
            name='TecContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tname', models.CharField(max_length=30, verbose_name='优秀实践标题')),
                ('tag', models.CharField(max_length=10, verbose_name='标签')),
                ('body', models.TextField(verbose_name='内容概括')),
                ('created_at', models.DateTimeField(verbose_name='时间')),
                ('file', models.FileField(upload_to=None, verbose_name='附件')),
                ('status', models.CharField(max_length=2, verbose_name='状态')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_post', to='account.UserInfo', verbose_name='作者')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='group_tec', to='account.Group', verbose_name='小组')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
