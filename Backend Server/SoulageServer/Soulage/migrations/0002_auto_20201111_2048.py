# Generated by Django 3.1.3 on 2020-11-11 15:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Soulage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verified_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 48, 1, 460181)),
        ),
        migrations.AlterField(
            model_name='donations',
            name='donated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 48, 1, 463203)),
        ),
        migrations.AlterField(
            model_name='poc_requests',
            name='decision_passed_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 48, 1, 464200)),
        ),
        migrations.AlterField(
            model_name='request',
            name='decision_passed_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 48, 1, 463203)),
        ),
        migrations.AlterField(
            model_name='request',
            name='initiated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 48, 1, 463203)),
        ),
        migrations.AlterField(
            model_name='topics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 48, 1, 462176)),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_time_stamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 11, 20, 48, 1, 460181)),
        ),
    ]
