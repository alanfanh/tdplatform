# Generated by Django 2.2.10 on 2020-05-12 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-course_time',), 'verbose_name': '培训课程', 'verbose_name_plural': '培训课程'},
        ),
    ]
