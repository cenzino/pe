# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0013_auto_20141007_0916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='voticandidato',
            options={'ordering': ['candidato__nome'], 'verbose_name_plural': 'VotiCandidato'},
        ),
        migrations.AddField(
            model_name='voticandidato',
            name='voti_mod',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
