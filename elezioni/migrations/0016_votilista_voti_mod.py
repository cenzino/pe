# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0015_elezione_aventi_diritto'),
    ]

    operations = [
        migrations.AddField(
            model_name='votilista',
            name='voti_mod',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
