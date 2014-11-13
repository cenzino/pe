# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0002_auto_20141006_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sezione',
            name='luogo',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
