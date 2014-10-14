from django.db import models
from django.db.models import Sum

class Elezione(models.Model):
    titolo = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=255, blank=True, null=False)
    chiusa = models.BooleanField(default=False)

    def voti_totali_candidati(self):
        return VotiCandidato.objects.filter(candidato__elezione_id=self.pk).aggregate(voti_totali=Sum('voti'))['voti_totali']

    def voti_totali_liste(self):
        return VotiLista.objects.filter(lista__elezione_id=self.pk).aggregate(voti_totali=Sum('voti'))['voti_totali']

    def media(self):
        media = 0.0
        for sezione in self.sezioni.all():
            media += sezione.totale_voti_scrutinati()*100.0/sezione.votanti

        return media/self.sezioni.count()

    def test(self):
        e = self.sezioni.annotate(vc=Sum('voticandidato__voti')).values('vc', 'se')

        return e

    def totale_votanti(self):
        return Sezione.objects.filter(elezione__pk=self.pk).aggregate(Sum('votanti'))['votanti__sum']

    def totale_iscritti(self):
        return Sezione.objects.filter(elezione__pk=self.pk).aggregate(Sum('aventi_diritto'))['aventi_diritto__sum']

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
    aventi_diritto = models.PositiveIntegerField(default=0)
    elezione = models.ForeignKey(Elezione, related_name="sezioni", related_query_name="sezione")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Sezione, self).save(*args, **kwargs)
        if is_new:
            VotiCandidato.objects.bulk_create(
                [VotiCandidato(candidato=candidato, sezione=self) for candidato in self.elezione.candidati.all()])
            VotiLista.objects.bulk_create(
                [VotiLista(lista=lista, sezione=self) for lista in self.elezione.liste.all()])

    def totale_voti_scrutinati(self):
        return VotiCandidato.objects.filter(sezione__pk=self.pk).aggregate(Sum('voti'))['voti__sum']

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

    def __str__(self):
        return "%s %s" % (self.cognome, self.nome)

    def voti_totali(self):
        return self.voticandidato_set.all().aggregate(Sum('voti'))['voti__sum']

    def voti_totali_liste(self):
        return VotiLista.objects.filter(lista__candidato__pk=self.pk).aggregate(Sum('voti'))['voti__sum']

    def get_media(self):
        return 30.5

    def get_forbice(self):
        import random
        return round(random.random()*2, 2)

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

    def voti_totali(self):
        return self.votilista_set.all().aggregate(Sum('voti'))['voti__sum']

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Liste"

    def __str__(self):
        return "%s" % (self.nome)

class VotiCandidato(models.Model):
    candidato = models.ForeignKey(Candidato)
    sezione = models.ForeignKey(Sezione)
    voti = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.candidato, self.sezione)

    class Meta:
        ordering = ['candidato__nome']
        verbose_name_plural = "VotiCandidato"

class VotiLista(models.Model):
    lista = models.ForeignKey(Lista)
    sezione = models.ForeignKey(Sezione)
    voti = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.lista, self.sezione)

    class Meta:
        verbose_name_plural = "VotiLista"