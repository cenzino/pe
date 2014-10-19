# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elezioni', '0024_auto_20141017_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatiProiezioneCandidato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voti', models.DecimalField(max_digits=3, decimal_places=1)),
                ('voti_liste', models.DecimalField(max_digits=3, decimal_places=1)),
                ('candidato', models.ForeignKey(to='elezioni.Candidato')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatiProiezioneLista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voti', models.DecimalField(max_digits=3, decimal_places=1)),
                ('lista', models.ForeignKey(to='elezioni.Lista')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proiezione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_creazione', models.DateTimeField(auto_created=True)),
                ('copertura', models.DecimalField(max_digits=3, decimal_places=1)),
                ('elezione', models.ForeignKey(to='elezioni.Elezione')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='datiproiezionelista',
            name='proiezione',
            field=models.ForeignKey(related_query_name=b'lista', related_name=b'liste', to='elezioni.Proiezione'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datiproiezionecandidato',
            name='proiezione',
            field=models.ForeignKey(related_query_name=b'candidato', related_name=b'candidati', to='elezioni.Proiezione'),
            preserve_default=True,
        ),
    ]
