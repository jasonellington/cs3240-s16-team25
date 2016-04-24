# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0005_reportfolder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='opened',
        ),
        migrations.AddField(
            model_name='message',
            name='bites',
            field=models.BinaryField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='encrypted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
