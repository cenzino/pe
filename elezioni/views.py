from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

from .models import *

# Create your views here.
def home(request):
    elezioni = Elezione.objects.all()
    #return render(request, 'index.html', { 'elezioni': elezioni})
    return render(request, 'login.html')

def login(request):
    #elezioni = Elezione.objects.all()
    return render(request, 'login.html')

def dettaglio(request, elezione_id):
    return HttpResponse("You're looking at question %s." % elezione_id)

def proiezioni_index(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    elezione.proiezioni.last()
    return render(request, 'proiezioni/candidati.html', { 'elezione': elezione })

def proiezioni_candidati2(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    elezione.aggiorna()
    candidati = elezione.candidati.all()
    return render(request, 'proiezioni/candidati2.html', { 'elezione': elezione, 'candidati': candidati })

def proiezioni_liste(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

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

from django.core import serializers

def crea_proiezione(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    p = Proiezione(elezione=elezione, copertura=0).save()
    data = serializers.serialize("json", Proiezione.objects.all())
    #return HttpResponse(data, content_type="application/json")
    return redirect('proiezioni_candidati', elezione_id=elezione_id)


def report_candidati(request, elezione_id, ponderati=False):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    elezione.pondera()

    return render(request, 'report/z.html', { 'elezione': elezione,
                                              'risultati': elezione.get_risultati(Candidato, False),
                                              'risultati2': elezione.get_risultati(Candidato, True)
    })

def report_liste(request, elezione_id, ponderati=False):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    elezione.pondera()

    return render(request, 'report/z.html', { 'elezione': elezione,
                                              'risultati': elezione.get_risultati(Lista, False),
                                              'risultati2': elezione.get_risultati(Lista, True)
    })