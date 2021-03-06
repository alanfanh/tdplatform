# Generated by Django 2.2.10 on 2020-06-30 10:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0005_auto_20200618_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='analysis_status',
            field=models.CharField(blank=True, max_length=10, verbose_name='是否分析'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='asset_number',
            field=models.CharField(blank=True, max_length=20, verbose_name='资产编号'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='closed_time',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='计划闭环时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='complaint',
            name='solutions',
            field=models.TextField(blank=True, verbose_name='改进措施'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='level',
            field=models.CharField(choices=[('高', 'high'), ('中', 'mid'), ('低', 'low')], max_length=50, verbose_name='严重程度'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='product',
            field=models.CharField(max_length=20, verbose_name='产品型号'),
        ),
    ]
