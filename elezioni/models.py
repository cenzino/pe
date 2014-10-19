from django.db import models
from django.db.models import Sum
from math import sqrt
from django.core import serializers

def calcola_forbice():
    pass

class Elezione(models.Model):
    titolo = models.CharField(max_length=255)
    descrizione = models.CharField(max_length=255, blank=True, null=False)
    chiusa = models.BooleanField(default=False)

    aventi_diritto = models.PositiveIntegerField(default=0)
    copertura_simulata = models.PositiveIntegerField(default=0, help_text="Simula la copertura del campione. Se uguale a 0 (predefinito) la copertura e' uguale alla media delle coperture delle sezioni.")
    intervallo_ricalcolo = models.PositiveIntegerField(default=1)

    def crea_proiezione(self):
        p = Proiezione(elezione=self)
        p.save()

    def c_get_copertura_campione(self):
        copertura = 0.0
        for sezione in self.sezioni.all():
            copertura += sezione.c_copertura()

        return copertura/self.sezioni.all().count()

    def pondera(self, candidati=False, liste=False):
        copertura_campione = self.c_get_copertura_campione()

        if candidati or liste:
            for sezione in self.sezioni.all():
                if candidati:
                    sezione.pondera_dati_candidati(copertura_campione)
                if liste:
                    sezione.pondera_dati_liste(copertura_campione)

    def get_risultati(self, cls, ponderati=False):
        elemento = cls._meta.model_name
        elementi = cls._meta.verbose_name_plural.lower()
        tipo = elementi_tipo = ''

        if ponderati:
            tipo = '_mod'
            elementi_tipo = '%s_%s' % (elementi, tipo)

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
                Sum('schede_nulle'),
                Sum('schede_bianche')
            )

        risultati = {
            #'nomi': risultati_sezioni[0].elementi[0],
            'sezioni':  risultati_sezioni,
            'totali': {
                'votanti': totali['votanti__sum'],
                'iscritti': totali['iscritti__sum'],
                'schede_bianche': totali['schede_bianche%s__sum' % (elementi_tipo)],
                'schede_nulle': totali['schede_nulle%s__sum' % (elementi_tipo)],
                'schede_valide': totali['schede_valide__sum'],
                'elementi': getattr(self, "%s" % (elementi)).select_related('voti%(elemento)s_set').annotate(rvoti=Sum('voti%s__voti%s' % (elemento, tipo)))
                #'elementi': VotiCandidato.objects.filter(candidato__elezione__pk=self.id).values('candidato__id').annotate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))

            }
        }
        return risultati


    def c_get_risultati_liste(self, tipo='grezzi'):
        risultati = {}
        risultati['origine'] = 'liste'

        if tipo == 'ponderati':
            _tipo = '_mod'
            _tipo_alt = '_mod_liste'
            risultati['tipo'] = 'ponderati'
        else:
            _tipo = _tipo_alt = ''

        sezioni = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide=Sum('votilista__voti%s'%_tipo))

        risultati['sezioni'] = []

        for sezione in sezioni.values():
            s = sezione
            s['schede_bianche'] = s['schede_bianche%s'%_tipo_alt]
            s['schede_nulle'] = s['schede_nulle%s'%_tipo_alt]
            s['schede_scrutinate'] = s['schede_valide']+s['schede_bianche']+s['schede_nulle']

            s['elementi'] = [ {'voti': v['voti%s'%_tipo]} for v in VotiLista.objects.filter(sezione__pk=sezione['id']).values('voti', 'voti_mod')]
            #print s['elementi']

            risultati['sezioni'].append(s)

        totali = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide_sum=Sum('votilista__voti%s'%_tipo)).aggregate(iscritti=Sum('iscritti'), votanti=Sum('votanti'), schede_nulle=Sum('schede_nulle%s'%_tipo_alt), schede_bianche=Sum('schede_bianche%s'%_tipo_alt), schede_valide=Sum('schede_valide_sum'))

        totali['schede_scrutinate'] = totali['schede_valide']+totali['schede_bianche']+totali['schede_nulle']

        totali['elementi'] = VotiLista.objects.filter(lista__elezione__pk=self.id).values('lista__id').annotate(voti=Sum('voti%s'%_tipo))

        risultati['sezioni'].append(totali)
        risultati['nomi'] = self.liste.all().values_list('nome')
        return risultati

    def c_get_risultati(self, tipo='grezzi'):
        risultati = {}
        risultati['origine'] = 'candidati'

        if tipo == 'ponderati':
            _tipo = '_mod'
            _tipo_alt = '_mod_candidati'
            risultati['tipo'] = 'ponderati'
        else:
            _tipo = _tipo_alt = ''


        sezioni = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide=Sum('voticandidato__voti%s'%_tipo))

        risultati['sezioni'] = []

        for sezione in sezioni.values():
            s = sezione
            s['schede_bianche'] = s['schede_bianche%s'%_tipo_alt]
            s['schede_nulle'] = s['schede_nulle%s'%_tipo_alt]
            s['schede_scrutinate'] = s['schede_valide']+s['schede_bianche']+s['schede_nulle']

            s['elementi'] = [ {'voti': v['voti%s'%_tipo]} for v in VotiCandidato.objects.filter(sezione__pk=sezione['id']).values('voti', 'voti_mod')]
            #wprint s['elementi']

            risultati['sezioni'].append(s)

        totali = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide_sum=Sum('voticandidato__voti%s'%_tipo)).aggregate(iscritti=Sum('iscritti'), votanti=Sum('votanti'), schede_nulle=Sum('schede_nulle%s'%_tipo_alt), schede_bianche=Sum('schede_bianche%s'%_tipo_alt), schede_valide=Sum('schede_valide_sum'))

        totali['schede_scrutinate'] = totali['schede_valide']+totali['schede_bianche']+totali['schede_nulle']

        totali['elementi'] = VotiCandidato.objects.filter(candidato__elezione__pk=self.id).values('candidato__id').annotate(voti=Sum('voti%s'%_tipo))

        risultati['sezioni'].append(totali)
        risultati['nomi'] = self.candidati.all().values_list('cognome')
        return risultati


    def c_get_risultati_candidati_full(self):
        risultati = {}
        risultati['origine'] = 'candidati'

        sezioni = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide=Sum('voticandidato__voti'), schede_valide_mod=Sum('voticandidato__voti_mod'))
        _sezioni = []

        for sezione in sezioni.values():
            _s = sezione
            #_s = {}
            _s['schede_nulle'] = {
                    'grezzi': sezione['schede_nulle'],
                    'ponderati': sezione['schede_nulle_mod_candidati']
                }
            _s['schede_bianche'] = {
                    'grezzi': sezione['schede_bianche'],
                    'ponderati': sezione['schede_bianche_mod_candidati']
                }
            _s['schede_valide'] = {
                    'grezzi': sezione['schede_valide'],
                    'ponderati': sezione['schede_valide_mod']
                }
            _s['schede_scrutinate'] = {
                    'grezzi': (_s['schede_valide']['grezzi']+_s['schede_nulle']['grezzi']+_s['schede_bianche']['grezzi']),
                    'ponderati': (_s['schede_valide']['ponderati']+_s['schede_nulle']['ponderati']+_s['schede_bianche']['ponderati'])
                }
            _s['elementi'] = [ {'voti': { 'grezzi': v['voti'], 'ponderati': v['voti_mod'] }} for v in VotiCandidato.objects.filter(sezione__pk=sezione['id']).values('voti', 'voti_mod')]

            _sezioni.append(_s)

        risultati['nomi'] = self.candidati.all().values_list('cognome')
        risultati['sezioni'] = _sezioni

        totali = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide_sum=Sum('voticandidato__voti'), schede_valide_mod_sum=Sum('voticandidato__voti_mod')).aggregate(iscritti=Sum('iscritti'), votanti=Sum('votanti'), schede_nulle_mod=Sum('schede_nulle_mod_candidati'), schede_nulle=Sum('schede_nulle'), schede_bianche=Sum('schede_bianche'), schede_bianche_mod=Sum('schede_bianche_mod_candidati'), schede_valide=Sum('schede_valide_sum'), schede_valide_mod=Sum('schede_valide_mod_sum'))
        _totali = totali
        _totali['schede_nulle'] = {
            'grezzi': totali['schede_nulle'],
            'ponderati': totali['schede_nulle_mod']
        }
        _totali['schede_bianche'] = {
            'grezzi': totali['schede_bianche'],
            'ponderati': totali['schede_bianche_mod']
        }
        _totali['schede_valide'] = {
            'grezzi': totali['schede_valide'],
            'ponderati': totali['schede_valide_mod']
        }
        _totali['schede_scrutinate'] = {
                'grezzi': (_totali['schede_valide']['grezzi']+_totali['schede_nulle']['grezzi']+_totali['schede_bianche']['grezzi']),
                'ponderati': (_totali['schede_valide']['ponderati']+_totali['schede_nulle']['ponderati']+_totali['schede_bianche']['ponderati'])
            }

        _totali['elementi'] = [ {'voti': {'grezzi': v['voti'], 'ponderati': v['voti_mod'] }} for v in VotiCandidato.objects.filter(candidato__elezione__pk=self.id).values('candidato__id').annotate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))]

        risultati['sezioni'].append(_totali)

        return risultati

    def c_get_risultati_liste_full(self):
        risultati = {}
        risultati['origine'] = 'liste'

        sezioni = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide=Sum('votilista__voti'), schede_valide_mod=Sum('votilista__voti_mod'))
        _sezioni = []

        for sezione in sezioni.values():
            _s = sezione
            #_s = {}
            _s['schede_nulle'] = {
                    'grezzi': sezione['schede_nulle'],
                    'ponderati': sezione['schede_nulle_mod_liste']
                }
            _s['schede_bianche'] = {
                    'grezzi': sezione['schede_bianche'],
                    'ponderati': sezione['schede_bianche_mod_liste']
                }
            _s['schede_valide'] = {
                    'grezzi': sezione['schede_valide'],
                    'ponderati': sezione['schede_valide_mod']
                }
            _s['schede_scrutinate'] = {
                    'grezzi': (_s['schede_valide']['grezzi']+_s['schede_nulle']['grezzi']+_s['schede_bianche']['grezzi']),
                    'ponderati': (_s['schede_valide']['ponderati']+_s['schede_nulle']['ponderati']+_s['schede_bianche']['ponderati'])
                }
            _s['elementi'] = [ {'voti': { 'grezzi': v['voti'], 'ponderati': v['voti_mod'] }} for v in VotiLista.objects.filter(sezione__pk=sezione['id']).values('voti', 'voti_mod')]

            _sezioni.append(_s)

        risultati['nomi'] = self.liste.all().values_list('nome')
        risultati['sezioni'] = _sezioni

        totali = Sezione.objects.filter(elezione__pk=self.pk).annotate(schede_valide_sum=Sum('votilista__voti'), schede_valide_mod_sum=Sum('votilista__voti_mod')).aggregate(iscritti=Sum('iscritti'), votanti=Sum('votanti'), schede_nulle_mod=Sum('schede_nulle_mod_liste'), schede_nulle=Sum('schede_nulle'), schede_bianche=Sum('schede_bianche'), schede_bianche_mod=Sum('schede_bianche_mod_liste'), schede_valide=Sum('schede_valide_sum'), schede_valide_mod=Sum('schede_valide_mod_sum'))
        _totali = totali
        _totali['schede_nulle'] = {
            'grezzi': totali['schede_nulle'],
            'ponderati': totali['schede_nulle_mod']
        }
        _totali['schede_bianche'] = {
            'grezzi': totali['schede_bianche'],
            'ponderati': totali['schede_bianche_mod']
        }
        _totali['schede_valide'] = {
            'grezzi': totali['schede_valide'],
            'ponderati': totali['schede_valide_mod']
        }
        _totali['schede_scrutinate'] = {
                'grezzi': (_totali['schede_valide']['grezzi']+_totali['schede_nulle']['grezzi']+_totali['schede_bianche']['grezzi']),
                'ponderati': (_totali['schede_valide']['ponderati']+_totali['schede_nulle']['ponderati']+_totali['schede_bianche']['ponderati'])
            }

        _totali['elementi'] = [ {'voti': {'grezzi': v['voti'], 'ponderati': v['voti_mod'] }} for v in VotiLista.objects.filter(lista__elezione__pk=self.id).values('lista__id').annotate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))]

        risultati['sezioni'].append(_totali)

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

    def z_get(self):
        self.z = 0
        return self

    def schede_valide_candidato(self):
        #return self.voticandidato_set.all().aggregate(voti=Sum('voti'))['voti']
        return VotiCandidato.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti'))['voti']

    def schede_valide_liste(self):
        return VotiLista.objects.filter(sezione__pk=self.pk).aggregate(voti=Sum('voti'))['voti']

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
        return (self.c_get_schede_valide_mod() + self.schede_bianche_mod_candidati + self.schede_nulle_mod_candidati)

    def c_copertura(self):
        return self.c_get_schede_scrutinate()*1.0/self.votanti

    def pondera_dati_candidati(self, copertura_campione=1.0):
        _schede_scrutinate_ponderate = self.votanti * copertura_campione

        _schede_valide_candidati = self.schede_valide_candidato()


        _schede_scrutinate_candidati = self.schede_nulle + self.schede_bianche + _schede_valide_candidati
        _schede_valide_candidati_ponderate = int(round(float(_schede_valide_candidati) / _schede_scrutinate_candidati * _schede_scrutinate_ponderate))

        self.schede_nulle_mod_candidati = 0 if self.schede_nulle==0 else int(round(_schede_scrutinate_ponderate * (float(self.schede_nulle)/_schede_scrutinate_candidati)))
        self.schede_bianche_mod_candidati = 0 if self.schede_bianche==0 else int(round(_schede_scrutinate_ponderate * (float(self.schede_bianche)/_schede_scrutinate_candidati)))

        self.save()

        for v in self.voticandidato_set.all():
            try:
                v.voti_mod = round(_schede_valide_candidati_ponderate * float(v.voti) / _schede_valide_candidati)
            except:
                v.voti_mod = 0
            v.save()

    def pondera_dati_liste(self, copertura_campione=1.0):
        _schede_scrutinate_ponderate = self.votanti * copertura_campione

        _schede_valide_liste = self.schede_valide_liste()


        _schede_scrutinate_liste = self.schede_nulle + self.schede_bianche + _schede_valide_liste
        _schede_valide_liste_ponderate = int(round(float(_schede_valide_liste) / _schede_scrutinate_liste * _schede_scrutinate_ponderate))

        self.schede_nulle_mod_liste = 0 if self.schede_nulle==0 else int(round(_schede_scrutinate_ponderate * (float(self.schede_nulle)/_schede_scrutinate_liste)))
        self.schede_bianche_mod_liste = 0 if self.schede_bianche==0 else int(round(_schede_scrutinate_ponderate * (float(self.schede_bianche)/_schede_scrutinate_liste)))

        self.save()

        for v in self.votilista_set.all():
            try:
                v.voti_mod = round(_schede_valide_liste_ponderate * float(v.voti) / _schede_valide_liste)
            except ZeroDivisionError:
                v.voti_mod = 0
            v.save()


    def c_aggiorna(self, copertura=1.0):
        copertura = copertura
        #print "copertura: %f " % copertura
        scrutinate = self.c_get_schede_scrutinate()
        #print "scrutinate: %s" % (scrutinate)
        scrutinate_ponderate = round(self.votanti*copertura)
        #print "scrutinate_ponderate: %i" % (scrutinate_ponderate)

        valide = self.c_get_schede_valide()
        #print "valide: %i" % (valide)

        valide_ponderate = round(valide*1.0/scrutinate * scrutinate_ponderate)
        #print "valide_ponderate: %f" % (valide_ponderate)

        self.schede_bianche_mod_candidati = 0

        if self.schede_bianche != 0:
            self.schede_bianche_mod_candidati = self.schede_bianche*1.0 / scrutinate * scrutinate_ponderate

        self.schede_nulle_mod_candidati = 0

        if self.schede_nulle != 0:
            self.schede_nulle_mod_candidati = self.schede_nulle*1.0 / scrutinate * scrutinate_ponderate

        self.save()

        for vc in self.voticandidato_set.all():
            vc.voti_mod = round(vc.voti*1.0 / valide * valide_ponderate)
            #print "voti_mod: %f" % (vc.voti_mod)
            vc.save()

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



    def _get_nome_short(self):
        return self.cognome

    nome_short = property(_get_nome_short)

    def __str__(self):
        return "%s" % (self.cognome)

    def voti_totali(self):
        return self.voticandidato_set.all().aggregate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))

    def voti_totali_liste(self):
        return VotiLista.objects.filter(lista__candidato__pk=self.pk).aggregate(voti=Sum('voti'), voti_mod=Sum('voti_mod'))


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
    elezione = models.ForeignKey(Elezione)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        #super(Proiezione, self).save(*args, **kwargs)

        if is_new:
            self.copertura = round(self.elezione.c_get_copertura_campione(), 3)
            print self.copertura
            super(Proiezione, self).save(*args, **kwargs)
            DatiProiezioneCandidato.objects.bulk_create(
                [DatiProiezioneCandidato(proiezione=self, candidato=candidato, voti=0.0, voti_liste=0.0) for candidato in self.elezione.candidati.all()]
            )
            """
            DatiProiezioneCandidato.objects.bulk_create(
                [DatiProiezioneCandidato(proiezione=self, lista=lista, voti=0.0) for lista in Lista.objects.filter(candidato__elezione__pk=self.elezione_id)]
            )
            """
            """
            VotiCandidato.objects.bulk_create(
                [VotiCandidato(candidato=candidato, sezione=self) for candidato in self.elezione.candidati.all()])
            VotiLista.objects.bulk_create(
                [VotiLista(lista=lista, sezione=self) for lista in self.elezione.liste.all()])
            """

class DatiProiezioneCandidato(models.Model):
    proiezione = models.ForeignKey(Proiezione, related_name='candidati', related_query_name='candidato')
    candidato = models.ForeignKey(Candidato)
    voti = models.DecimalField(max_digits=3, decimal_places=1)
    voti_liste = models.DecimalField(max_digits=3, decimal_places=1)

class DatiProiezioneLista(models.Model):
    proiezione = models.ForeignKey(Proiezione, related_name='liste', related_query_name='lista')
    lista = models.ForeignKey(Lista)
    voti = models.DecimalField(max_digits=3, decimal_places=1)