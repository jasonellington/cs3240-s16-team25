# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0009_message_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportfile',
            name='hash',
            field=models.CharField(null=True, max_length=40, default=None),
            preserve_default=True,
        ),
    ]
