from django.db import models
from django.db.models import Sum, Max
from math import sqrt
from django.core import serializers

class Elezione(models.Model):
    titolo = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=255, blank=True, null=False)
    chiusa = models.BooleanField(default=False)

    aventi_diritto = models.PositiveIntegerField(default=0)
    copertura_simulata = models.PositiveIntegerField(default=0, help_text="Simula la copertura del campione. Se uguale a 0 (predefinito) la copertura e' uguale alla media delle coperture delle sezioni.")
    intervallo_ricalcolo = models.PositiveIntegerField(default=1)

    def get_copertura_campione(self):
        if self.copertura_simulata != 0:
            return self.copertura_simulata*0.01

        risultati_sezioni = self.sezioni.select_related('voticandidato_set').annotate(
            schede_valide=Sum('voticandidato__voti')
        )

        copertura = 0.0
        for sezione in risultati_sezioni:
            copertura += float(sezione.schede_valide + sezione.schede_nulle + sezione.schede_bianche)/sezione.votanti

        return copertura/risultati_sezioni.count()

    def _pondera(self, cls):
        elemento = cls._meta.model_name
        elementi = cls._meta.verbose_name_plural.lower()

        copertura_campione = self.get_copertura_campione()

        risultati_sezioni = self.sezioni.select_related('voti%(elemento)s_set').annotate(
            schede_valide=Sum('voti%s__voti' % (elemento))
        )

        print risultati_sezioni.values()

        for sezione in risultati_sezioni:
            schede_scrutinate = sezione.schede_valide + sezione.schede_nulle + sezione.schede_bianche
            _schede_scrutinate_ponderate = sezione.votanti * copertura_campione
            _ponderazione = float(_schede_scrutinate_ponderate)/schede_scrutinate
            _valide = sezione.schede_valide*_ponderazione

            setattr(sezione, 'schede_nulle_mod_%s' % (elementi), round(sezione.schede_nulle * _ponderazione))
            setattr(sezione, 'schede_bianche_mod_%s' % (elementi), round(sezione.schede_bianche * _ponderazione))

            _elementi = getattr(sezione, "voti%s_set" % (elemento)).select_related('%(elemento)s').annotate(rvoti=Sum('voti'))

            sezione.save()

            for e in _elementi:
                try:
                    _ponderazione_voti = float(_valide)/sezione.schede_valide
                except ZeroDivisionError:
                    _ponderazione_voti = 0
                setattr(e, 'voti_mod', round(e.rvoti*_ponderazione_voti))
                e.save()

    def get_risultati(self, cls, ponderati=False):
        self._pondera(cls)
        elemento = cls._meta.model_name
        elementi = cls._meta.verbose_name_plural.lower()

        tipo = elementi_tipo = ''

        if ponderati:
            tipo = '_mod'
            elementi_tipo = '%s_%s' % (tipo, elementi)

        risultati_sezioni = self.sezioni.select_related('voti%(elemento)s_set').annotate(
            schede_valide=Sum('voti%s__voti%s' % (elemento, tipo))
        )

        for sezione in risultati_sezioni:
            sezione.schede_nulle = getattr(sezione, "schede_nulle%s" % (elementi_tipo))
            sezione.schede_bianche = getattr(sezione, "schede_bianche%s" % (elementi_tipo))
            sezione.elementi = getattr(sezione, "voti%s_set" % (elemento)).select_related('%(elemento)s').annotate(rvoti=Sum('voti%s' % (tipo)))

        totali = risultati_sezioni.aggregate(
                Sum('iscritti'),
                Sum('votanti'),
                Sum('schede_valide'),
                Sum('schede_nulle%s' % (elementi_tipo)),
                Sum('schede_bianche%s' % (elementi_tipo))
            )

        risultati = {
            'sezioni':  risultati_sezioni,
            'totali': {
                'votanti': totali['votanti__sum'],
                'iscritti': totali['iscritti__sum'],
                'schede_bianche': totali['schede_bianche%s__sum' % (elementi_tipo)],
                'schede_nulle': totali['schede_nulle%s__sum' % (elementi_tipo)],
                'schede_valide': totali['schede_valide__sum'],
                'elementi': getattr(self, "%s" % (elementi)).select_related('voti%(elemento)s_set').annotate(rvoti=Sum('voti%s__voti%s' % (elemento, tipo)))

            }
        }
        return risultati

    def __str__(self):
        return self.titolo

    class Meta:
        verbose_name_plural = "Elezioni"

class Sezione(models.Model):
    numero = models.PositiveSmallIntegerField()
    nome = models.CharField(max_length=100)
    luogo = models.CharField(max_length=255, blank=True)
    attiva = models.BooleanField(default=True)
    votanti = models.PositiveIntegerField(default=0)
    iscritti = models.PositiveIntegerField(default=0)
    elezione = models.ForeignKey(Elezione, related_name="sezioni", related_query_name="sezione")

    schede_nulle = models.PositiveIntegerField(default=0)
    schede_bianche = models.PositiveIntegerField(default=0)

    schede_nulle_mod_candidati = models.PositiveIntegerField(default=0)
    schede_bianche_mod_candidati = models.PositiveIntegerField(default=0)

    schede_nulle_mod_liste = models.PositiveIntegerField(default=0)
    schede_bianche_mod_liste = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Sezione, self).save(*args, **kwargs)
        if is_new:
            VotiCandidato.objects.bulk_create(
                [VotiCandidato(candidato=candidato, sezione=self) for candidato in self.elezione.candidati.all()])
            VotiLista.objects.bulk_create(
                [VotiLista(lista=lista, sezione=self) for lista in self.elezione.liste.all()])

    def __str__(self):
        return "%i %s" % (self.numero, self.nome)

    class Meta:
        ordering = ['numero']
        verbose_name_plural = "Sezioni"

class Candidato(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='images/foto/', blank=True, null=True)
    voti_sezione = models.ManyToManyField(Sezione, through='VotiCandidato', related_name="voti_candidato", related_query_name="voto_candidato")
    elezione = models.ForeignKey(Elezione, related_name="candidati", related_query_name="candidato")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Candidato, self).save(*args, **kwargs)
        if is_new:
            VotiCandidato.objects.bulk_create(
                [VotiCandidato(candidato=self, sezione=sezione) for sezione in self.elezione.sezioni.all()])

    def _get_nome_short(self):
        return self.cognome

    nome_short = property(_get_nome_short)

    def __str__(self):
        return "%s" % (self.cognome)

    class Meta:
        ordering = ['cognome']
        verbose_name_plural = "Candidati"

class Lista(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=20, blank=True)
    simbolo = models.ImageField(upload_to='images/simboli/', blank=True, null=True)
    voti_sezione = models.ManyToManyField(Sezione, through='VotiLista', related_name="voti_lista", related_query_name="voto_lista")
    elezione = models.ForeignKey(Elezione, related_name="liste", related_query_name="lista")
    candidato = models.ForeignKey(Candidato, related_name="liste", related_query_name="lista")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Lista, self).save(*args, **kwargs)

        if is_new:
            VotiLista.objects.bulk_create(
                [VotiLista(lista=self, sezione=sezione) for sezione in self.elezione.sezioni.all()])

    class Meta:
        #ordering = ['nome']
        verbose_name_plural = "Liste"

    def __str__(self):
        return "%s" % (self.nome)

class VotiCandidato(models.Model):
    candidato = models.ForeignKey(Candidato)
    sezione = models.ForeignKey(Sezione)
    voti = models.IntegerField(default=0)
    voti_mod = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.candidato, self.sezione)

    class Meta:
        ordering = ['candidato__cognome']
        verbose_name_plural = "VotiCandidato"

class VotiLista(models.Model):
    lista = models.ForeignKey(Lista)
    sezione = models.ForeignKey(Sezione)
    voti = models.IntegerField(default=0)
    voti_mod = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.lista, self.sezione)

    class Meta:
        verbose_name_plural = "VotiLista"

class Proiezione(models.Model):
    data_creazione = models.DateTimeField(auto_now_add=True)
    copertura = models.DecimalField(max_digits=4, decimal_places=3)
    elezione = models.ForeignKey(Elezione, related_name='proiezioni', related_query_name='proiezione')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Proiezione, self).save(*args, **kwargs)
        if is_new:
            candidati = self.elezione.candidati.select_related('voticandidato_set', 'lista_set').order_by('id').annotate(voti_totali=Sum('voticandidato__voti_mod'))
            liste = self.elezione.liste.select_related('candidato','votilista').annotate(voti_totali=Sum('votilista__voti_mod'))

            totale_voti_liste_per_candidato = liste.values('candidato').order_by('candidato_id').annotate(voti_totali=Sum('votilista__voti_mod'))
            totale_voti_liste = liste.aggregate(totale=Sum('voti_totali'))['totale']

            totale_voti_candidati = candidati.aggregate(totale=Sum('voti_totali'))['totale']

            _candidati = []

            aventi_diritto_totali = self.elezione.aventi_diritto
            totali_candidati = self.elezione.sezioni.aggregate(nulle=Sum('schede_nulle_mod_candidati'),bianche=Sum('schede_bianche_mod_candidati'))
            _totale_scrutinate_candidati = totale_voti_candidati + totali_candidati['nulle'] + totali_candidati['bianche']

            if liste:
                totali_liste = self.elezione.sezioni.aggregate(nulle=Sum('schede_nulle_mod_liste'),bianche=Sum('schede_bianche_mod_liste'))
                _totale_scrutinate_liste = totale_voti_liste + totali_candidati['nulle'] + totali_candidati['bianche']

            for i, candidato in enumerate(candidati):
                _forbice = calcola_forbice(aventi_diritto_totali, _totale_scrutinate_candidati, candidato.voti_totali)
                _voti_liste = totale_voti_liste_per_candidato[i]['voti_totali'] if totale_voti_liste_per_candidato else 0
                _forbice_liste = calcola_forbice(aventi_diritto_totali, _totale_scrutinate_liste, _voti_liste) if liste else 0
                _candidati.append(DatiProiezioneCandidato(candidato=candidato, proiezione=self,
                                                          voti=round(float(candidato.voti_totali)/totale_voti_candidati*100, 1),
                                                          voti_liste=round(float(_voti_liste)/totale_voti_liste*100, 1) if liste else 0,
                                                          forbice=_forbice,
                                                          forbice_liste=_forbice_liste if liste else 0
                                                          ))
            DatiProiezioneCandidato.objects.bulk_create(_candidati)

            if liste:

                _liste = []
                for lista in liste:
                    _forbice = calcola_forbice(aventi_diritto_totali, _totale_scrutinate_liste, lista.voti_totali)
                    _liste.append(DatiProiezioneLista(lista=lista, proiezione=self,
                                                      voti=round(float(lista.voti_totali)/totale_voti_liste*100, 1),
                                                      forbice=_forbice))
                DatiProiezioneLista.objects.bulk_create(_liste)

    def test(self):
        pass

class DatiProiezioneCandidato(models.Model):
    proiezione = models.ForeignKey(Proiezione, related_name='candidati', related_query_name='candidato')
    candidato = models.ForeignKey(Candidato)
    voti = models.DecimalField(max_digits=3, decimal_places=1)
    voti_liste = models.DecimalField(max_digits=3, decimal_places=1)
    forbice = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    forbice_liste = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

class DatiProiezioneLista(models.Model):
    proiezione = models.ForeignKey(Proiezione, related_name='liste', related_query_name='lista')
    lista = models.ForeignKey(Lista)
    voti = models.DecimalField(max_digits=3, decimal_places=1)
    forbice = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)


def calcola_forbice(aventi_diritto_totali, totale_voti_scrutinati, voti_totali_elemento):
    percentuale_elemento = float(voti_totali_elemento)/totale_voti_scrutinati

    f = percentuale_elemento * float(1 - percentuale_elemento) / totale_voti_scrutinati
    g = 1 - (float(totale_voti_scrutinati)/ aventi_diritto_totali )

    percentile = 1.96 * sqrt(f) * sqrt(g)
    return percentile*100