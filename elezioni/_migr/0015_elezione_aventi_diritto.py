# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0014_auto_20141014_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='elezione',
            name='aventi_diritto',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
