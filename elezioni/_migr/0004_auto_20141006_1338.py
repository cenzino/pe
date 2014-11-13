# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0003_auto_20141006_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista',
            name='sigla',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
