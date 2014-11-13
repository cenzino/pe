from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required

from .models import *
from utenti.models import *

@login_required(login_url='/login/')
def home(request):
    elezioni = Elezione.objects.all()
    #if request.user:
        #print request.user
        #print request.user.has_perms(['proiezioni','report','rilevazione'])
        #print request.user.has_perms(['cippalippa'])
    #return render(request, 'index.html', { 'elezioni': elezioni })
    #return render(request, 'login.html')

    #return redirect('proiezioni_home', elezione_id=1)
    #return redirect('rilevazione_home', sezione_id=1)
    print request.user.tipo
    if request.user.tipo == 'Rilevatore':
        return redirect('rilevazione_home')
    elif request.user.tipo == 'Ricercatore':
        return redirect('report_home')
    elif request.user.tipo == 'Emittente':
        return redirect('proiezioni_home')
    elif request.user.tipo == 'Utente':
        return render(request, 'index.html', { 'elezioni': elezioni })
    else:
        pass
    #return redirect('report_home', elezione_id=1)

"""
def login(request):
    return render(request, 'login.html')
"""

# ### PROIEZIONI
# ### ==================================================

def proiezioni_home(request):
    print request.user.tipo
    user = request.user
    if user.tipo == 'Emittente':
        emittente = get_object_or_404(Emittente, pk=user.id)
        elezioni = Elezione.objects.all()

    print emittente.pk

    return HttpResponse('Proiezioni Home')

def proiezioni_candidati(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    return render(request, 'proiezioni/candidati.html', { 'elezione': elezione })

def proiezioni_liste(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    return render(request, 'proiezioni/liste.html', { 'elezione': elezione })

def proiezioni_candidato_one(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    candidato = elezione.proiezioni.last

    return render(request, 'proiezioni/candidati_one.html', { 'elezione': elezione, 'candidato': candidato })

def proiezioni_candidato(request, elezione_id, candidato_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    candidato = get_object_or_404(Candidato, pk=candidato_id)
    proiezione = Proiezione.objects.filter(elezione_id=elezione.id).last()
    daticandidato = DatiProiezioneCandidato.objects.filter(proiezione_id=proiezione.id, candidato_id=candidato.id).first()
    datiliste = DatiProiezioneLista.objects.filter(lista__candidato_id=candidato.id, proiezione_id=proiezione.id).all()

    return render(request, 'proiezioni/candidato.html', { 'elezione': elezione, 'candidato': daticandidato, 'proiezione': proiezione, 'liste': datiliste })

# ### RILEVAZIONE
# ### ==================================================

def rilevazione_home(request):
    user = request.user
    if user.tipo == 'Rilevatore':
        pass
    return HttpResponse('Rilevazione Home')


def rilevazione_index(request, sezione_id):
    sezione = get_object_or_404(Sezione, pk=sezione_id)
    return render(request, 'rilevazione/test.html', {'sezione': sezione})

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

# ### REPORT
# ### ==================================================


def report_home(request):
    return HttpResponse('Report Home')

def crea_proiezione(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    p = Proiezione(elezione=elezione, copertura=0).save()
    data = serializers.serialize("json", Proiezione.objects.all())
    #return HttpResponse(data, content_type="application/json")
    return redirect('report_home', elezione_id=elezione_id)


def report_candidati(request, elezione_id, ponderati=False):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    elezione._pondera(Candidato)

    return render(request, 'report/report.html', { 'elezione': elezione,
                                              'risultati': elezione.get_risultati(Candidato, False),
                                              'risultati2': elezione.get_risultati(Candidato, True)
    })

def report_liste(request, elezione_id, ponderati=False):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    elezione._pondera(Lista)

    return render(request, 'report/report.html', { 'elezione': elezione,
                                              'risultati': elezione.get_risultati(Lista, False),
                                              'risultati2': elezione.get_risultati(Lista, True)
    })

from django.conf import settings
import time

def test(request):
    print request.POST
    if request.is_ajax():
        if getattr(settings, 'DEBUG', False): # only if DEBUG=True
            import time
            import random
            #time.sleep(random.randint(0,4)) # delay AJAX response for 5 seconds
        print "Ajax"
        try:
            id = int(request.POST['vid'])
            v = get_object_or_404(VotiCandidato, pk=id)
            op = str(request.POST['op'])

            voti = v.voti + (1 if op == 'inc' else -1)
            if voti >= 0:
                v.voti = voti
                v.save()
            #board_pk = int(request.POST['board'])
            #moves = list(map(int, request.POST['move_list'].split(',')))
        except KeyError:
            return HttpResponse('Error') # incorrect post
        # do stuff, e.g. calculate a score
        return HttpResponse(v.voti)
    else:
        raise Http404

def test2(request):
    print request.POST
    if request.is_ajax():
        if getattr(settings, 'DEBUG', False): # only if DEBUG=True
            import time
            import random
            #time.sleep(random.randint(0,2)) # delay AJAX response for 5 seconds
        print "Ajax"
        try:
            id = int(request.POST['vid'])
            v = get_object_or_404(VotiLista, pk=id)
            op = str(request.POST['op'])

            voti = v.voti + (1 if op == 'inc' else -1)
            if voti >= 0:
                v.voti = voti
                v.save()
            #board_pk = int(request.POST['board'])
            #moves = list(map(int, request.POST['move_list'].split(',')))
        except KeyError:
            return HttpResponse('Error') # incorrect post
        # do stuff, e.g. calculate a score
        return HttpResponse(v.voti)
    else:
        raise Http404


from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

# index view (just redirect to login page)
def index(request):
  return HttpResponseRedirect('/login')

# this view will run after successfull login
@login_required
def logged_in(request):
    return redirect('home')
    """
    return render_to_response('logged_in.html',
        context_instance=RequestContext(request)
    )
    """