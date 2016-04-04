# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0002_auto_20160330_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='admin',
        ),
    ]
