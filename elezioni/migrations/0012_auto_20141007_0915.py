# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0011_auto_20141007_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidato',
            name='voti_sezione',
            field=models.ManyToManyField(related_query_name=b'voto_candidato', related_name=b'voti_candidato', through='elezioni.VotiCandidato', to=b'elezioni.Sezione'),
        ),
        migrations.AlterField(
            model_name='lista',
            name='voti_sezione',
            field=models.ManyToManyField(related_query_name=b'voto_lista', related_name=b'voti_lista', through='elezioni.VotiLista', to=b'elezioni.Sezione'),
        ),
    ]
