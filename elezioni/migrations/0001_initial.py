# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import elezioni.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
                ('cognome', models.CharField(max_length=50)),
                ('foto', models.ImageField(null=True, upload_to=elezioni.models._get_image_path, blank=True)),
            ],
            options={
                'ordering': ['cognome'],
                'verbose_name_plural': 'Candidati',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatiProiezioneCandidato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voti', models.DecimalField(max_digits=3, decimal_places=1)),
                ('voti_liste', models.DecimalField(max_digits=3, decimal_places=1)),
                ('forbice', models.DecimalField(default=0.0, max_digits=3, decimal_places=1)),
                ('forbice_liste', models.DecimalField(default=0.0, max_digits=3, decimal_places=1)),
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
                ('forbice', models.DecimalField(default=0.0, max_digits=3, decimal_places=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Elezione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=255)),
                ('descrizione', models.CharField(max_length=255, blank=True)),
                ('chiusa', models.BooleanField(default=False)),
                ('aventi_diritto', models.PositiveIntegerField(default=0)),
                ('copertura_simulata', models.PositiveIntegerField(default=0, help_text=b"Simula la copertura del campione. Se uguale a 0 (predefinito) la copertura e' uguale alla media delle coperture delle sezioni.")),
                ('intervallo_ricalcolo', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name_plural': 'Elezioni',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
                ('sigla', models.CharField(max_length=20, blank=True)),
                ('simbolo', models.ImageField(null=True, upload_to=elezioni.models._get_image_path, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Liste',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proiezione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('copertura', models.DecimalField(max_digits=4, decimal_places=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sezione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.PositiveSmallIntegerField()),
                ('nome', models.CharField(max_length=100)),
                ('luogo', models.CharField(max_length=255, blank=True)),
                ('attiva', models.BooleanField(default=True)),
                ('votanti', models.PositiveIntegerField(default=0)),
                ('iscritti', models.PositiveIntegerField(default=0)),
                ('schede_nulle', models.PositiveIntegerField(default=0)),
                ('schede_bianche', models.PositiveIntegerField(default=0)),
                ('schede_nulle_mod_candidati', models.PositiveIntegerField(default=0, editable=False)),
                ('schede_bianche_mod_candidati', models.PositiveIntegerField(default=0, editable=False)),
                ('schede_nulle_mod_liste', models.PositiveIntegerField(default=0, editable=False)),
                ('schede_bianche_mod_liste', models.PositiveIntegerField(default=0, editable=False)),
                ('elezione', models.ForeignKey(related_query_name=b'sezione', related_name=b'sezioni', to='elezioni.Elezione')),
            ],
            options={
                'ordering': ['numero'],
                'verbose_name_plural': 'Sezioni',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VotiCandidato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voti', models.IntegerField(default=0)),
                ('voti_mod', models.IntegerField(default=0, editable=False)),
                ('candidato', models.ForeignKey(to='elezioni.Candidato')),
                ('sezione', models.ForeignKey(to='elezioni.Sezione')),
            ],
            options={
                'ordering': ['candidato__cognome'],
                'verbose_name_plural': 'VotiCandidato',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VotiLista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voti', models.IntegerField(default=0)),
                ('voti_mod', models.IntegerField(default=0, editable=False)),
                ('lista', models.ForeignKey(to='elezioni.Lista')),
                ('sezione', models.ForeignKey(to='elezioni.Sezione')),
            ],
            options={
                'verbose_name_plural': 'VotiLista',
            },
            bases=(models.Model,),
        ),
    ]
