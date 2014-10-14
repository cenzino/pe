# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0010_auto_20141007_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='elezione',
            field=models.ForeignKey(related_query_name=b'candidato', related_name=b'candidati', to='elezioni.Elezione'),
        ),
        migrations.AlterField(
            model_name='lista',
            name='candidato',
            field=models.ForeignKey(related_query_name=b'lista', related_name=b'liste', to='elezioni.Candidato'),
        ),
        migrations.AlterField(
            model_name='lista',
            name='elezione',
            field=models.ForeignKey(related_query_name=b'lista', related_name=b'liste', to='elezioni.Elezione'),
        ),
        migrations.AlterField(
            model_name='sezione',
            name='elezione',
            field=models.ForeignKey(related_query_name=b'sezione', related_name=b'sezioni', to='elezioni.Elezione'),
        ),
    ]
