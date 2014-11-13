# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0009_auto_20141007_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sezione',
            name='elezione',
            field=models.ForeignKey(to='elezioni.Elezione'),
        ),
    ]
