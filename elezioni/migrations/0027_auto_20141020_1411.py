# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0026_auto_20141019_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='datiproiezionecandidato',
            name='forbice',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datiproiezionelista',
            name='forbice',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=1),
            preserve_default=True,
        ),
    ]
