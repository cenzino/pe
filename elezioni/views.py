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


def report_candidati_dati_grezzi(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.c_aggiorna()
    risultati = elezione.c_get_risultati()
    return render(request, 'report/index.html', { 'elezione': elezione, 'risultati': risultati })

def report_candidati_dati_ponderati(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.c_aggiorna()
    elezione.pondera(candidati=True)
    risultati = elezione.c_get_risultati_candidati_full()
    return render(request, 'report/index.html', { 'elezione': elezione, 'risultati': risultati })

def report_liste_dati_grezzi(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.c_aggiorna()
    risultati = elezione.c_get_risultati_liste()
    return render(request, 'report/index.html', { 'elezione': elezione, 'risultati': risultati })

def report_liste_dati_ponderati(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.c_aggiorna()
    elezione.crea_proiezione()
    elezione.pondera(liste=True)
    risultati = elezione.c_get_risultati_liste_full()
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

#--------------
def report_test(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    elezione.pondera(candidati=True)
    #elezione.aggiorna()
    #elezione.c_aggiorna()
    risultati = {}
    sezioni = []

    risultati = elezione.c_get_risultati()
    risultati2 = elezione.c_get_risultati('ponderati')
    return render(request, 'report/test.html', { 'elezione': elezione, 'risultati': risultati, 'risultati2': risultati2 })
#---------------

def report_test_liste(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.aggiorna()
    #elezione.c_aggiorna()
    elezione.pondera(liste=True)
    risultati = elezione.c_get_risultati_liste()
    risultati2 = elezione.c_get_risultati_liste('ponderati')
    return render(request, 'report/test.html', { 'elezione': elezione, 'risultati': risultati, 'risultati2': risultati2 })


def report_test3(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    #elezione.aggiorna()
    #elezione.c_aggiorna()
    elezione.pondera()
    risultati = elezione.c_get_risultati_candidati_full()
    data = risultati

    return render(request, 'report/test3.html', { 'risultati': risultati })

def z(request, elezione_id):
    elezione = get_object_or_404(Elezione.objects.select_related('sezioni'), pk=elezione_id)

    return render(request, 'report/z.html', { 'elezione': elezione, 'risultati': elezione.get_risultati(Candidato) })