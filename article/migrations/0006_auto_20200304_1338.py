# Generated by Django 2.2.8 on 2020-03-04 05:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20200304_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 4, 5, 38, 36, 132125, tzinfo=utc)),
        ),
    ]
