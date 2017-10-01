# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='right_answer_counts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='wrong_answer_counts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]