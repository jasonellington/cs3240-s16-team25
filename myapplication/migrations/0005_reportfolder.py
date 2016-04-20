# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapplication', '0004_auto_20160417_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportFolder',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('reports', models.ManyToManyField(to='myapplication.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
