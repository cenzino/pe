# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0030_auto_20141021_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='datiproiezionecandidato',
            name='forbice_liste',
            field=models.DecimalField(default=0.0, max_digits=3, decimal_places=1),
            preserve_default=True,
        ),
    ]
