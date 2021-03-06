# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-24 15:39
from __future__ import unicode_literals

from django.db import migrations, models

from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0009_auto_20180403_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now(), verbose_name='Created date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated date'),
        ),
    ]
