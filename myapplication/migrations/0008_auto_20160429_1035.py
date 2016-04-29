# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapplication', '0007_auto_20160425_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('poster', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('reporton', models.ForeignKey(to='myapplication.Report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='views',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
    ]
