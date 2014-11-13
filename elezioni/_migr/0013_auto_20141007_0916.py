# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0012_auto_20141007_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elezione',
            name='descrizione',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
