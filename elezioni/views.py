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
    candidati = elezione.candidati.all()
    return render(request, 'proiezioni/index.html', { 'elezione': elezione, 'candidati': candidati })

def proiezioni_candidati2(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
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
    SezioneForm = modelform_factory(Sezione, fields=("votanti", "aventi_diritto"))
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
    return render(request, 'report/index.html', { 'elezione': elezione })

def report_test(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    return render(request, 'report/test.html', { 'elezione': elezione })