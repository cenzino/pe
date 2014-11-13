# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0016_votilista_voti_mod'),
    ]

    operations = [
        migrations.AddField(
            model_name='elezione',
            name='copertura_simulata',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
