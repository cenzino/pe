# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0019_auto_20141015_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='elezione',
            name='intervallo_ricalcolo',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
