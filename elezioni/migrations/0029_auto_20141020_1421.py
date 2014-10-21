# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0028_auto_20141020_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datiproiezionecandidato',
            name='forbice',
            field=models.DecimalField(default=0.0, max_digits=3, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='datiproiezionelista',
            name='forbice',
            field=models.DecimalField(default=0.0, max_digits=3, decimal_places=1),
        ),
    ]
