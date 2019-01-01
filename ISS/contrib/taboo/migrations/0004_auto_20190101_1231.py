# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-01 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taboo', '0003_tabooviolationrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabooviolationrecord',
            name='loser_former_title',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tabooviolationrecord',
            name='titles_rectified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tabooviolationrecord',
            name='victor_former_title',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
    ]
