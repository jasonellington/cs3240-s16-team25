# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapplication', '0010_reportfile_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('phone_number', models.CharField(max_length=11, default=None, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
