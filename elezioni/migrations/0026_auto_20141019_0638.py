# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0025_auto_20141017_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proiezione',
            name='copertura',
            field=models.DecimalField(max_digits=4, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='proiezione',
            name='data_creazione',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
