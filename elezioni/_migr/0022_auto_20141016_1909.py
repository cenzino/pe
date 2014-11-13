# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0021_auto_20141015_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidato',
            options={'verbose_name_plural': 'Candidati'},
        ),
        migrations.AlterModelOptions(
            name='lista',
            options={'verbose_name_plural': 'Liste'},
        ),
        migrations.AlterModelOptions(
            name='voticandidato',
            options={'verbose_name_plural': 'VotiCandidato'},
        ),
        migrations.RenameField(
            model_name='sezione',
            old_name='schede_bianche_mod',
            new_name='schede_bianche_mod_candidati',
        ),
        migrations.RenameField(
            model_name='sezione',
            old_name='schede_nulle_mod',
            new_name='schede_nulle_mod_candidati',
        ),
    ]
