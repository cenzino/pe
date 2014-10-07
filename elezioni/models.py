from django.db import models

class Elezione(models.Model):
    titolo = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=255, blank=False, null=False)
    chiusa = models.BooleanField(default=False)

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
    elezione = models.ForeignKey(Elezione)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Sezione, self).save(*args, **kwargs)
        if is_new:
            VotiCandidato.objects.bulk_create(
                [VotiCandidato(candidato=candidato, sezione=self) for candidato in self.elezione.candidato_set.all()])
            VotiLista.objects.bulk_create(
                [VotiLista(lista=lista, sezione=self) for lista in self.elezione.lista_set.all()])

    def __str__(self):
        return "%i %s" % (self.numero, self.nome)

    class Meta:
        ordering = ['numero']
        verbose_name_plural = "Sezioni"

class Candidato(models.Model):
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='images/foto/', blank=True, null=True)
    voti_sezione = models.ManyToManyField(Sezione, through='VotiCandidato')
    elezione = models.ForeignKey(Elezione)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Candidato, self).save(*args, **kwargs)
        if is_new:
            VotiCandidato.objects.bulk_create(
                [VotiCandidato(candidato=self, sezione=sezione) for sezione in self.elezione.sezione_set.all()])

    def __str__(self):
        return "%s %s" % (self.cognome, self.nome)

    class Meta:
        ordering = ['cognome']
        verbose_name_plural = "Candidati"

class Lista(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=20, blank=True)
    simbolo = models.ImageField(upload_to='images/simboli/', blank=True, null=True)
    voti_sezione = models.ManyToManyField(Sezione, through='VotiLista')
    elezione = models.ForeignKey(Elezione)
    candidato = models.ForeignKey(Candidato)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Lista, self).save(*args, **kwargs)

        if is_new:
            VotiLista.objects.bulk_create(
                [VotiLista(lista=self, sezione=sezione) for sezione in self.elezione.sezione_set.all()])

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
        #ordering = ['cognome']
        verbose_name_plural = "VotiCandidato"

class VotiLista(models.Model):
    lista = models.ForeignKey(Lista)
    sezione = models.ForeignKey(Sezione)
    voti = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.lista, self.sezione)

    class Meta:
        verbose_name_plural = "VotiLista"