# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapplication', '0006_auto_20160424_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='permittedUsers'),
            preserve_default=True,
        ),
    ]
