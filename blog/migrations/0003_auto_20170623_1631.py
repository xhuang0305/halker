# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 08:31
from __future__ import unicode_literals

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20170621_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
