# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0023_auto_20141016_1915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidato',
            options={'ordering': ['cognome'], 'verbose_name_plural': 'Candidati'},
        ),
        migrations.AlterModelOptions(
            name='voticandidato',
            options={'ordering': ['candidato__cognome'], 'verbose_name_plural': 'VotiCandidato'},
        ),
    ]
