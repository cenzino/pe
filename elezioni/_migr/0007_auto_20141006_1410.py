# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0006_auto_20141006_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sezione',
            name='attiva',
            field=models.BooleanField(default=True),
        ),
    ]
