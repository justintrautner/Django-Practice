# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-17 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='creator',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='books', to='belt.User'),
            preserve_default=False,
        ),
    ]
