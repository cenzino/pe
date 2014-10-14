# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0008_auto_20141007_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sezione',
            name='elezione',
            field=models.ForeignKey(related_name=b'sezioni', to='elezioni.Elezione'),
        ),
    ]
