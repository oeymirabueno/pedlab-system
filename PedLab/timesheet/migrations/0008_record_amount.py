# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-28 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0007_payment_date_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Amount'),
        ),
    ]