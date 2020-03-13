# Generated by Django 2.2.8 on 2020-03-04 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200229_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rank_name', models.CharField(max_length=5, verbose_name='职级')),
            ],
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='engineer',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='job_num',
            field=models.CharField(blank=True, max_length=8, verbose_name='工号'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_group', to='account.Group', verbose_name='用户所属组'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_role', to='account.Role', verbose_name='用户角色'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='rank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_rank', to='account.Rank', verbose_name='用户职级'),
            preserve_default=False,
        ),
    ]