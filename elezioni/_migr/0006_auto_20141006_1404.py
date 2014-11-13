# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0005_auto_20141006_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lista',
            old_name='voti_sezioni',
            new_name='voti_sezione',
        ),
    ]
