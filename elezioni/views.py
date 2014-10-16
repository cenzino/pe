from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .models import *

# Create your views here.
def home(request):
    elezioni = Elezione.objects.all()
    return render(request, 'index.html', { 'elezioni': elezioni})

def dettaglio(request, elezione_id):
    return HttpResponse("You're looking at question %s." % elezione_id)

def proiezioni_index(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    elezione.aggiorna()
    candidati = elezione.candidati.all()
    sponsor = ["Sponsor %s" % (s+1) for s in range(8) ]
    return render(request, 'proiezioni/index.html', { 'elezione': elezione, 'candidati': candidati, 'sponsor': sponsor })

def proiezioni_candidati2(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    elezione.aggiorna()
    candidati = elezione.candidati.all()
    return render(request, 'proiezioni/candidati2.html', { 'elezione': elezione, 'candidati': candidati })

def proiezioni_liste(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    elezione.aggiorna()
    candidati = elezione.candidati.all()
    return render(request, 'proiezioni/liste.html', { 'elezione': elezione, 'candidati': candidati })

def rilevazione_index(request, sezione_id):
    sezione = get_object_or_404(Sezione, pk=sezione_id)
    return render(request, 'rilevazione/index.html', { 'sezione': sezione})

def aumentaVotoCandidato(request, votocandidato_id):
    voto_candidato = get_object_or_404(VotiCandidato, pk=votocandidato_id)
    voto_candidato.voti += 1
    voto_candidato.save()
    return redirect('rilevazione_index', sezione_id=voto_candidato.sezione.id)

def diminuisciVotoCandidato(request, votocandidato_id):
    voto_candidato = get_object_or_404(VotiCandidato, pk=votocandidato_id)
    voto_candidato.voti -= 1
    voto_candidato.save()
    return redirect('rilevazione_index', sezione_id=voto_candidato.sezione.id)

def aumentaVotoLista(request, votolista_id):
    voto_lista = get_object_or_404(VotiLista, pk=votolista_id)
    voto_lista.voti += 1
    voto_lista.save()
    return redirect('rilevazione_index', sezione_id=voto_lista.sezione.id)

def diminuisciVotoLista(request, votolista_id):
    voto_lista = get_object_or_404(VotiLista, pk=votolista_id)
    voto_lista.voti -= 1
    voto_lista.save()
    return redirect('rilevazione_index', sezione_id=voto_lista.sezione.id)

from django.forms.models import modelform_factory

def edita_sezione(request, sezione_id):
    SezioneForm = modelform_factory(Sezione, fields=("votanti", "iscritti"))
    sezione = get_object_or_404(Sezione, pk=sezione_id)

    if request.method == 'POST':
        form = SezioneForm(request.POST, instance=sezione)
        if form.is_valid():
            form.save()
            return render(request, 'rilevazione/edita_sezione.html', { 'sezione': sezione, 'form': form})
    else:
        form = SezioneForm(instance=sezione)

    return render(request, 'rilevazione/edita_sezione.html', { 'sezione': sezione, 'form': form})


def report(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.c_aggiorna()
    risultati = elezione.c_get_risultati()
    return render(request, 'report/index.html', { 'elezione': elezione, 'risultati': risultati })

def report_liste(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.aggiorna()
    return render(request, 'report/liste.html', { 'elezione': elezione })

from django.core import serializers
def data(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    data = serializers.serialize("json", elezione.sezioni.all(), indent=4, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return HttpResponse(data, content_type='application/json')
    #return HttpResponse(simplejson.dumps(shipments, ensure_ascii=False, default=json_formatter), mimetype='application/json')

def report_test(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.aggiorna()
    #elezione.c_aggiorna()
    risultati = {}
    sezioni = []
    """
    for sezione in elezione.sezioni.all():
        s = {
            'numero': sezione.numero,
            'iscritti': sezione.iscritti,
            'votanti': sezione.votanti,
            'schede_valide': sezione.c_get_schede_valide(),
            'schede_bianche': sezione.schede_bianche,
            'schede_nulle': sezione.schede_nulle
        }
        s['schede_scrutinate'] = s['schede_valide'] + s['schede_nulle'] + s['schede_bianche']
        elementi = []
        for voti in sezione.voticandidato_set.all():
            #print voti.voti
            elemento = {
                'voti': voti.voti,
            }
            elementi.append(elemento)
        s['elementi'] = elementi
        sezioni.append(s)
    risultati['nomi'] = elezione.candidati.values()
    risultati['sezioni'] = sezioni

    risultati2 = {}
    sezioni2 = []
    """
    """
    for sezione in elezione.sezioni.all():
        s = {
            'numero': sezione.numero,
            'iscritti': sezione.iscritti,
            'votanti': sezione.votanti,
            'schede_valide': sezione.c_get_schede_valide_mod(),
            'schede_bianche': sezione.schede_bianche_mod,
            'schede_nulle': sezione.schede_nulle_mod
        }
        s['schede_scrutinate'] = s['schede_valide'] + s['schede_nulle'] + s['schede_bianche']
        #s['schede']['scrutinate'] = elezione.c_get_copertura_campione()*sezione.votanti
        elementi = []
        for voti in sezione.voticandidato_set.all():
            #print voti.voti
            elemento = {
                'voti': voti.voti_mod,
            }
            elementi.append(elemento)
        s['elementi'] = elementi
        sezioni2.append(s)
    risultati2['nomi'] = elezione.candidati.values()
    risultati2['sezioni'] = sezioni2
    """
    risultati = elezione.c_get_risultati()
    risultati2 = elezione.c_get_risultati('ponderati')
    return render(request, 'report/test.html', { 'elezione': elezione, 'risultati': risultati, 'risultati2': risultati2 })