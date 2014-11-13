# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0027_auto_20141020_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datiproiezionecandidato',
            name='forbice',
            field=models.DecimalField(max_digits=3, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='datiproiezionelista',
            name='forbice',
            field=models.DecimalField(max_digits=3, decimal_places=1),
        ),
    ]
