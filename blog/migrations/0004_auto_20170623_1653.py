# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 08:53
from __future__ import unicode_literals

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170623_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='created_time',
        ),
        migrations.RemoveField(
            model_name='post',
            name='modified_time',
        ),
        migrations.AddField(
            model_name='post',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='post',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
