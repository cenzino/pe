# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0020_elezione_intervallo_ricalcolo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sezione',
            name='schede_bianche_mod',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sezione',
            name='schede_nulle_mod',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
