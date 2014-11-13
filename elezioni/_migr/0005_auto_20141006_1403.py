# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0004_auto_20141006_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidato',
            old_name='votiSezioni',
            new_name='voti_sezione',
        ),
        migrations.RenameField(
            model_name='lista',
            old_name='votiSezioni',
            new_name='voti_sezioni',
        ),
    ]
