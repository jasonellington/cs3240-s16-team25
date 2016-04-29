# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0008_auto_20160429_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='viewed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
