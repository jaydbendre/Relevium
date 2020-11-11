# Generated by Django 3.1.3 on 2020-11-11 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Soulage', '0002_auto_20201111_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donations',
            name='donated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 57, 46, 976408)),
        ),
        migrations.AlterField(
            model_name='poc_requests',
            name='decision_passed_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 57, 46, 976408)),
        ),
        migrations.AlterField(
            model_name='request',
            name='decision_passed_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 57, 46, 975413)),
        ),
        migrations.AlterField(
            model_name='request',
            name='initiated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 57, 46, 975413)),
        ),
        migrations.AlterField(
            model_name='topics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 57, 46, 974416)),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 57, 46, 973382)),
        ),
        migrations.AlterField(
            model_name='user',
            name='verified_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 57, 46, 973382)),
        ),
    ]
