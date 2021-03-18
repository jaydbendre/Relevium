# Generated by Django 3.0 on 2021-03-18 16:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Soulage', '0010_auto_20210317_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poc_requests',
            name='uid',
        ),
        migrations.AddField(
            model_name='poc_requests',
            name='name',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='data_collection',
            name='stored_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
        migrations.AlterField(
            model_name='donations',
            name='donated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
        migrations.AlterField(
            model_name='poc_requests',
            name='decision_passed_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
        migrations.AlterField(
            model_name='request',
            name='decision_passed_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
        migrations.AlterField(
            model_name='request',
            name='initiated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
        migrations.AlterField(
            model_name='topics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
        migrations.AlterField(
            model_name='user',
            name='verified_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 18, 22, 27, 17, 255615)),
        ),
    ]
