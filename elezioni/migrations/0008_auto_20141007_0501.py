# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0007_auto_20141006_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista',
            name='candidato',
            field=models.ForeignKey(to='elezioni.Candidato'),
        ),
    ]
