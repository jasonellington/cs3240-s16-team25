# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0002_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('Nval', models.TextField()),
                ('Eval', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
