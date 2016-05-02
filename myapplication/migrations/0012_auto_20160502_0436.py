# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0011_usernumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernumber',
            name='phone_number',
            field=models.CharField(default=None, max_length=13, null=True),
        ),
    ]
