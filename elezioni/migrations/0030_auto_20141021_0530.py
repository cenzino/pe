# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0029_auto_20141020_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proiezione',
            name='elezione',
            field=models.ForeignKey(related_query_name=b'proiezione', related_name=b'proiezioni', to='elezioni.Elezione'),
        ),
    ]
