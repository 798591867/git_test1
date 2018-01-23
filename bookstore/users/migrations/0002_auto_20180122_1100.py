# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='username',
            field=models.CharField(verbose_name='用户名', max_length=20, unique=True),
        ),
    ]
