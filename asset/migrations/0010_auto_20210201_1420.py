# Generated by Django 2.2.10 on 2021-02-01 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0009_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='bbit_round',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tr4_round',
        ),
        migrations.AddField(
            model_name='project',
            name='delay_percent',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='项目偏差率'),
        ),
        migrations.AddField(
            model_name='project',
            name='deliver',
            field=models.DateField(blank=True, null=True, verbose_name='性能板交付时间'),
        ),
        migrations.AddField(
            model_name='project',
            name='tec',
            field=models.TextField(blank=True, null=True, verbose_name='技术项目'),
        ),
        migrations.AddField(
            model_name='project',
            name='test_round',
            field=models.IntegerField(blank=True, null=True, verbose_name='测试轮次'),
        ),
        migrations.AlterField(
            model_name='project',
            name='completed_time',
            field=models.DateField(blank=True, null=True, verbose_name='TR5/6时间'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateField(verbose_name='立项时间'),
        ),
    ]
