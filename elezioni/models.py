from django.db import models
from django.db.models import Sum
from math import sqrt

class Elezione(models.Model):
    titolo = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=255, blank=True, null=False)
    chiusa = models.BooleanField(default=False)

    aventi_diritto = models.PositiveIntegerField(default=0)
    copertura_simulata = models.PositiveIntegerField(default=0, help_text="Simula la copertura del campione. Se uguale a 0 (predefinito) la copertura e' uguale alla media delle coperture delle sezioni.")
    intervallo_ricalcolo = models.PositiveIntegerField(default=1)

    def c_get_copertura_campione(self):
        copertura = 0.0
        for sezione in self.sezioni.all():
            copertura += sezione.c_copertura()

        return copertura/self.sezioni.all().count()

    def c_get_risultati(self, tipo='grezzi'):
        if tipo == 'ponderati':
            _tipo = '_mod'
        else:
            _tipo = ''

        risultati = {}
        sezioni = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide=Sum('voticandidato__voti%s'%_tipo))

        risultati['sezioni'] = []

        for sezione in sezioni.values():
            s = sezione
            s['schede_bianche'] = s['schede_bianche%s'%_tipo]
            s['schede_nulle'] = s['schede_nulle%s'%_tipo]
            s['schede_scrutinate'] = s['schede_valide']+s['schede_bianche']+s['schede_nulle']

            s['elementi'] = [ {'voti': v['voti%s'%_tipo]} for v in VotiCandidato.objects.filter(sezione__pk=sezione['id']).values('voti', 'voti_mod')]
            print s['elementi']

            risultati['sezioni'].append(s)

        totali = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide_sum=Sum('voticandidato__voti%s'%_tipo)).aggregate(iscritti=Sum('iscritti'), votanti=Sum('votanti'), schede_nulle=Sum('schede_nulle%s'%_tipo), schede_bianche=Sum('schede_bianche%s'%_tipo), schede_valide=Sum('schede_valide_sum'))

        totali['schede_scrutinate'] = totali['schede_valide']+totali['schede_bianche']+totali['schede_nulle']

        totali['elementi'] = VotiCandidato.objects.filter(candidato__elezione__pk=self.id).values('candidato__id').annotate(voti=Sum('voti%s'%_tipo))

        risultati['sezioni'].append(totali)
        risultati['nomi'] = self.candidati.all().values()
        return risultati




    def voti_totali_candidati(self):
        return VotiCandidato.objects.filter(candidato__elezione_id=self.pk).aggregate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))

    def voti_totali_liste(self):
        return VotiLista.objects.filter(lista__elezione_id=self.pk).aggregate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))

    def totale_schede(self):
        return Sezione.objects.filter(elezione__pk=self.pk).aggregate(bianche=Sum('schede_bianche'), nulle=Sum('schede_nulle'))

    def totale_schede_scrutinate(self):
        voti = VotiCandidato.objects.filter(candidato__elezione_id=self.pk).aggregate(voti=Sum('voti'))['voti']
        schede = self.totale_schede()
        return voti + schede['bianche'] + schede['nulle']

    def copertura(self):
        if self.copertura_simulata != 0:
            return self.copertura_simulata*0.01

        copertura = 0.0
        i = 0
        for sezione in self.sezioni.all():
            copertura += sezione.copertura()
            i+=1

        return copertura/i
    """
    def test(self):
        e = self.sezioni.annotate(vc=Sum('voticandidato__voti')).values('vc', 'se')

        return e
    """
    def totale_votanti(self):
        return Sezione.objects.filter(elezione__pk=self.pk).aggregate(Sum('votanti'))['votanti__sum']

    def totale_iscritti(self):
        return Sezione.objects.filter(elezione__pk=self.pk).aggregate(Sum('iscritti'))['iscritti__sum']

    def __str__(self):
        return self.titolo

    def aggiorna(self):
        for sezione in self.sezioni.all():
            sezione.aggiorna(self.copertura())

    def c_aggiorna(self):
        for sezione in self.sezioni.all():
            sezione.c_aggiorna(self.c_get_copertura_campione())

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

    schede_nulle_mod = models.PositiveIntegerField(default=0)
    schede_bianche_mod = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Sezione, self).save(*args, **kwargs)
        if is_new:
            VotiCandidato.objects.bulk_create(
                [VotiCandidato(candidato=candidato, sezione=self) for candidato in self.elezione.candidati.all()])
            VotiLista.objects.bulk_create(
                [VotiLista(lista=lista, sezione=self) for lista in self.elezione.liste.all()])

    def c_get_schede_valide(self):
        """Calcola il numero di schede valide scrutinate nella sezione

        Il valore corrisponde alla somma dei voti ai candidati della sezione
        """
        return VotiCandidato.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti'))['voti']

    def c_get_schede_valide_mod(self):
        """Calcola il numero di schede valide scrutinate nella sezione

        Il valore corrisponde alla somma dei voti ai candidati della sezione
        """
        return VotiCandidato.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti_mod'))['voti']

    def c_get_schede_scrutinate(self):
        """Calcola il numero di schede scrutinate nella sezione

        Il valore corrisponde alla somma dei voti ai candidati, delle schede nulle e delle schede bianche
        """
        return (self.c_get_schede_valide() + self.schede_bianche + self.schede_nulle)

    def c_get_schede_scrutinate_mod(self):
        """Calcola il numero di schede scrutinate nella sezione

        Il valore corrisponde alla somma dei voti ai candidati, delle schede nulle e delle schede bianche
        """
        return (self.c_get_schede_valide_mod() + self.schede_bianche_mod + self.schede_nulle_mod)

    def c_copertura(self):
        return self.c_get_schede_scrutinate()*1.0/self.votanti

    def c_aggiorna(self, copertura=1.0):
        copertura = copertura
        print "copertura: %f " % copertura
        scrutinate = self.c_get_schede_scrutinate()
        print "scrutinate: %s" % (scrutinate)
        scrutinate_ponderate = round(self.votanti*copertura)
        print "scrutinate_ponderate: %i" % (scrutinate_ponderate)

        valide = self.c_get_schede_valide()
        print "valide: %i" % (valide)

        valide_ponderate = round(valide*1.0/scrutinate * scrutinate_ponderate)
        print "valide_ponderate: %f" % (valide_ponderate)

        self.schede_bianche_mod = 0

        if self.schede_bianche != 0:
            self.schede_bianche_mod = self.schede_bianche*1.0 / scrutinate * scrutinate_ponderate

        self.schede_nulle_mod = 0

        if self.schede_nulle != 0:
            self.schede_nulle_mod = self.schede_nulle*1.0 / scrutinate * scrutinate_ponderate

        self.save()

        for vc in self.voticandidato_set.all():
            vc.voti_mod = round(vc.voti*1.0 / valide * valide_ponderate)
            print "voti_mod: %f" % (vc.voti_mod)
            vc.save()

        print

    def totale_voti_scrutinati(self):
        voti = VotiCandidato.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti'),voti_mod=Sum('voti_mod'))
        return voti

    def totale_schede_scrutinate(self):
        voti = VotiCandidato.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti'))
        return voti['voti'] + self.schede_nulle + self.schede_bianche

    def schede(self):
        schede = {}
        schede['valide'] = VotiCandidato.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti'))['voti']
        schede['nulle'] = self.schede_nulle
        schede['bianche'] = self.schede_bianche
        schede['totale'] = schede['valide'] + self.schede_nulle + self.schede_bianche
        return schede

    def get_copertura_mod(self):
        return round(self.votanti * self.elezione.copertura())

    def get_schede_valide_mod(self):
        voti = self.totale_voti_scrutinati()
        return int(round(voti['voti_mod']*voti['voti']*1.0/self.totale_schede_scrutinate()))

    def get_schede_bianche_mod(self):
        voti = self.totale_voti_scrutinati()
        return int(round(voti['voti_mod']*self.schede_bianche*1.0/self.totale_schede_scrutinate()))

    def get_schede_nulle_mod(self):
        voti = self.totale_voti_scrutinati()
        return int(round(voti['voti_mod']*self.schede_nulle*1.0/self.totale_schede_scrutinate()))

    def totale_voti_scrutinati_liste(self):
        return VotiLista.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti'),voti_mod=Sum('voti_mod'))

    def copertura(self):
        return self.totale_voti_scrutinati()['voti']*1.0/self.votanti

    def __str__(self):
        return "%i %s" % (self.numero, self.nome)

    def aggiorna(self, copertura=1.0):
        #print "Aggiornamento %s" % { self.nome }
        #vmod = self.votanti*copertura*1.0
        vmod = self.votanti*copertura*1.0
        #print "vmod: %1.f" % vmod
        #print "valide: %1.f" % self.get_schede_valide_mod()
        #print
        #vmod = self.get_schede_valide_mod()*1.0
        for vc in self.voticandidato_set.all():
            vc.voti_mod = vc.voti*1.0 / self.get_copertura_mod()*100
            #print "t: %f" % vc.voti_mod
            #vc.voti_mod = round(vmod*(vc.voti*1.0/self.totale_voti_scrutinati()['voti']))
            vc.save()
        for vl in self.votilista_set.all():
            t = self.totale_voti_scrutinati_liste()['voti']
            if t == 0:
                t = 1
            vl.voti_mod = round(vmod*(vl.voti*1.0/t))
            vl.save()

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
        return self.voticandidato_set.all().aggregate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))

    def voti_totali_liste(self):
        return VotiLista.objects.filter(lista__candidato__pk=self.pk).aggregate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))

    def get_media(self):
        return 30.5


    def get_forbice(self):
        #import random
        #return round(random.random()*2, 2)

        costante = 1.96
        aventi_diritto_totali = self.elezione.aventi_diritto
        totale_voti_scrutinati = self.elezione.voti_totali_candidati()['voti_mod']
        percentuale_candidato = self.voti_totali()['voti_mod']*1.0 / totale_voti_scrutinati

        #print self.cognome
        #print "aventi_diritto_totali: %f" % aventi_diritto_totali
        #print "totale_voti_scrutinati: %f" % totale_voti_scrutinati
        #print "percentuale_candidato: %f" % percentuale_candidato

        # f = percentuale_candidato * (1 - percentuale_candidato) / totale_voti_scrutinati
        f = percentuale_candidato * (1 - percentuale_candidato) / totale_voti_scrutinati
        #print "f: %f" % f

        # g = 1 - (totale_voti_scrutinati / aventi_diritto_totali )
        g = 1 - (totale_voti_scrutinati*1.0 / aventi_diritto_totali )
        #print "g: %f" % g

        percentile = costante * sqrt(f) * sqrt(g)
        return percentile*100

    class Meta:
        #ordering = ['cognome']
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
        return self.votilista_set.all().aggregate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))

    class Meta:
        #ordering = ['nome']
        verbose_name_plural = "Liste"

    def __str__(self):
        return "%s" % (self.nome)


    def get_forbice(self):
        #import random
        #return round(random.random()*2, 2)

        costante = 1.96
        aventi_diritto_totali = self.elezione.aventi_diritto
        totale_voti_scrutinati = self.elezione.voti_totali_candidati()['voti_mod']
        percentuale_candidato = self.voti_totali()['voti_mod']*1.0 / totale_voti_scrutinati

        #print self.cognome
        #print "aventi_diritto_totali: %f" % aventi_diritto_totali
        #print "totale_voti_scrutinati: %f" % totale_voti_scrutinati
        #print "percentuale_candidato: %f" % percentuale_candidato

        # f = percentuale_candidato * (1 - percentuale_candidato) / totale_voti_scrutinati
        f = percentuale_candidato * (1 - percentuale_candidato) / totale_voti_scrutinati
        #print "f: %f" % f

        # g = 1 - (totale_voti_scrutinati / aventi_diritto_totali )
        g = 1 - (totale_voti_scrutinati*1.0 / aventi_diritto_totali )
        #print "g: %f" % g

        percentile = costante * sqrt(f) * sqrt(g)
        return percentile*100


class VotiCandidato(models.Model):
    candidato = models.ForeignKey(Candidato)
    sezione = models.ForeignKey(Sezione)
    voti = models.IntegerField(default=0)
    voti_mod = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.candidato, self.sezione)

    class Meta:
        #ordering = ['candidato__nome']
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