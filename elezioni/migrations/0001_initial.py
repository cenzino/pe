# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
                ('foto', models.ImageField(null=True, upload_to=b'images/foto/', blank=True)),
            ],
            options={
                'ordering': ['cognome'],
                'verbose_name_plural': 'Candidati',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Elezione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=255)),
                ('descrizione', models.TextField()),
                ('chiusa', models.BooleanField(default=False)),
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
                ('sigla', models.CharField(max_length=20)),
                ('simbolo', models.ImageField(null=True, upload_to=b'images/simboli/', blank=True)),
                ('candidato', models.ForeignKey(to='elezioni.Candidato', null=True)),
                ('elezione', models.ForeignKey(to='elezioni.Elezione')),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name_plural': 'Liste',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sezione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.PositiveSmallIntegerField()),
                ('nome', models.CharField(max_length=100)),
                ('luogo', models.CharField(max_length=255)),
                ('attiva', models.BooleanField(default=False)),
                ('votanti', models.PositiveIntegerField(default=0)),
                ('aventi_diritto', models.PositiveIntegerField(default=0)),
                ('elezione', models.ForeignKey(to='elezioni.Elezione')),
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
                ('candidato', models.ForeignKey(to='elezioni.Candidato')),
                ('sezione', models.ForeignKey(to='elezioni.Sezione')),
            ],
            options={
                'verbose_name_plural': 'VotiCandidato',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VotiLista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('voti', models.IntegerField(default=0)),
                ('lista', models.ForeignKey(to='elezioni.Lista')),
                ('sezione', models.ForeignKey(to='elezioni.Sezione')),
            ],
            options={
                'verbose_name_plural': 'VotiLista',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lista',
            name='votiSezioni',
            field=models.ManyToManyField(to='elezioni.Sezione', through='elezioni.VotiLista'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidato',
            name='elezione',
            field=models.ForeignKey(to='elezioni.Elezione'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidato',
            name='votiSezioni',
            field=models.ManyToManyField(to='elezioni.Sezione', through='elezioni.VotiCandidato'),
            preserve_default=True,
        ),
    ]
