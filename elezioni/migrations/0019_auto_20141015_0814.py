# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0018_auto_20141015_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='sezione',
            name='schede_bianche',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sezione',
            name='schede_nulle',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
