# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-15 23:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0008_auto_20160615_2307'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formsubmission',
            options={'ordering': ['-date_received']},
        ),
    ]
