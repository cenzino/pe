# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0017_elezione_copertura_simulata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sezione',
            old_name='aventi_diritto',
            new_name='iscritti',
        ),
        migrations.AlterField(
            model_name='elezione',
            name='copertura_simulata',
            field=models.PositiveIntegerField(default=0, help_text=b"Simula la copertura del campione. Se uguale a 0 (predefinito) la copertura e' uguale alla media delle coperture delle sezioni."),
        ),
    ]
