# -*- coding: utf-8 -*-
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from .models import *
from django.core.exceptions import PermissionDenied

from django.utils import timezone

def is_member_of(user, group_name, exclusive=True):
    if exclusive:
        return user.groups.filter(name=group_name).count() == 1
    return user.groups.filter(name=group_name).exists()

def has_only_perm(user, perm_name):
    user.get_all_permissions().intersection(config.DEFAULT_SYSTEM_PERMISSIONS_NAME).difference(set([u'elezioni.%s' % (perm_name)]))

@login_required(login_url='/login/')
def home(request):
    user = request.user

    #print "* "*10
    #print set(config.DEFAULT_SYSTEM_PERMISSIONS_NAME).intersection(user.get_all_permissions())

    if user.is_superuser:
        return render(request, 'index.html', { 'elezioni': Elezione.objects.all() })

    if set(config.DEFAULT_SYSTEM_PERMISSIONS_NAME).intersection(user.get_all_permissions()):
        if is_member_of(user, config.RICERCATORI) or has_only_perm(user, config.CAN_VIEW_REPORTS[0]):
            #print "E' un ricercatore"
            return redirect('report_home')
        elif is_member_of(user, config.RILEVATORI) or has_only_perm(user, config.CAN_UPDATE_VOTES[0]):
            #print "E' un rilevatore"
            return redirect('rilevazione_home')
        elif is_member_of(user, config.EMITTENTI) or has_only_perm(user, config.CAN_VIEW_PROJECTIONS[0]):
            #print "E' un emittente"
            return redirect('proiezioni_home')
        return render(request, 'index.html', { 'elezioni': Elezione.objects.all() })

    raise PermissionDenied

# ### PROIEZIONI
# ### ==================================================

@login_required(login_url='/login/')
@permission_required('elezioni.can_view_projections','/login/', True)
def proiezioni_home(request):
    user = request.user

    if user.is_superuser:
        elezioni = Elezione.aperte.all()
    elif is_member_of(user, config.EMITTENTI):
        elezioni = Elezione.aperte.filter(emittenti__in=[user]).distinct()
    elif is_member_of(user, config.RICERCATORI):
        elezioni = Elezione.aperte.filter(ricercatori__in=[user]).distinct()
    else:
        elezioni = Elezione.aperte.all()

    if elezioni.count() == 1:

        return redirect('proiezioni_candidati', elezione_id=elezioni.first().id)

    return render(request, 'index.html', {'elezioni': elezioni})

@login_required(login_url='/login/')
@permission_required('elezioni.can_view_projections','/login/', True)
def proiezioni_candidati(request, elezione_id, proiezione_id=1):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    if request.user.is_superuser:
        proiezione = Proiezione.objects.filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.RICERCATORI):
        proiezione = Proiezione.objects.filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.EMITTENTI):
        proiezione = Proiezione.objects.filter(elezione_id=1, pubblicata=True).order_by('data_pubblicazione').last()

    return render(request, 'proiezioni/_candidati.html', { 'elezione': elezione, 'proiezione': proiezione })

@login_required(login_url='/login/')
@permission_required('elezioni.can_view_projections','/login/', True)
def proiezioni_liste(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    if request.user.is_superuser:
        proiezione = Proiezione.objects.select_related().filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.RICERCATORI):
        proiezione = Proiezione.objects.select_related().filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.EMITTENTI):
        proiezione = Proiezione.objects.select_related().filter(elezione_id=1, pubblicata=True).order_by('data_pubblicazione').last()
    else:
        raise PermissionDenied

    if not proiezione:
        return render(request, 'proiezioni/_candidati.html', { 'elezione': elezione, 'proiezione': proiezione })

    return render(request, 'proiezioni/liste.html', { 'elezione': elezione, 'proiezione': proiezione })



@login_required(login_url='/login/')
@permission_required('elezioni.can_view_projections','/login/', True)
def proiezioni_candidato_one(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    if request.user.is_superuser:
        proiezione = Proiezione.objects.filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.RICERCATORI):
        proiezione = Proiezione.objects.filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.EMITTENTI):
        proiezione = Proiezione.objects.filter(elezione_id=1, pubblicata=True).order_by('data_pubblicazione').last()
    else:
        raise PermissionDenied

    if proiezione:
        candidato = elezione.proiezioni.last
    else:
        return render(request, 'proiezioni/_candidati.html', { 'elezione': elezione, 'proiezione': proiezione })


    return render(request, 'proiezioni/__candidati_one.html', { 'elezione': elezione, 'proeiezione': proiezione, 'candidato': candidato })


@login_required(login_url='/login/')
@permission_required('elezioni.can_view_projections','/login/', True)
def proiezioni_candidato(request, elezione_id, candidato_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    candidato = get_object_or_404(Candidato, pk=candidato_id)

    if request.user.is_superuser:
        proiezione = Proiezione.objects.filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.RICERCATORI):
        proiezione = Proiezione.objects.filter(elezione_id=elezione_id).order_by('data_pubblicazione').last()
    elif is_member_of(request.user, config.EMITTENTI):
        proiezione = Proiezione.objects.filter(elezione_id=1, pubblicata=True).order_by('data_pubblicazione').last()
    else:
        raise PermissionDenied

    if proiezione:
        daticandidato = DatiProiezioneCandidato.objects.filter(proiezione_id=proiezione.id, candidato_id=candidato.id).first()
        datiliste = DatiProiezioneLista.objects.filter(lista__candidato_id=candidato.id, proiezione_id=proiezione.id).all()
    else:
        return render(request, 'proiezioni/_candidati.html', { 'elezione': elezione, 'proiezione': proiezione })

    return render(request, 'proiezioni/_candidato.html', { 'elezione': elezione, 'candidato': daticandidato, 'proiezione': proiezione, 'liste': datiliste })

# ### RILEVAZIONE
# ### ==================================================
@login_required()
@permission_required('elezioni.can_update_votes','/login/', True)
def rilevazione_home(request):
    user = request.user
    is_rilevatore = False

    if user.is_superuser:
        elezioni = Elezione.aperte.all()
    elif is_member_of(user, config.RICERCATORI):
        elezioni = Elezione.aperte.filter(ricercatori__in=[user]).distinct()
    elif is_member_of(user, config.RILEVATORI):
        elezioni = Elezione.objects.prefetch_related('sezioni').filter(sezione__rilevatore=user).distinct()
        is_rilevatore = True
    else:
        elezioni = Elezione.aperte.all()

    if elezioni.count() == 1:
        if is_rilevatore:
            sezioni = Sezione.objects.filter(rilevatore=user).all()
            if sezioni.count() == 1:
                return redirect('rilevazione_index', sezione_id=sezioni.first().id)
        #return redirect('rilevazione_index', sezione_id=sezioni.first().id)
        #return render(request, 'index.html', { 'elezioni': elezioni  })

    return render(request, 'index.html', { 'elezioni': elezioni, 'is_rilevatore': is_rilevatore })

    """
    #sezioni = Sezione.objects.filter(rilevatore_id=request.user.id, elezione__chiusa=False).all()

    if user.is_superuser:
        #sezioni = Sezione.objects.select_related('elezione').filter(elezione__chiusa=False).all() #.values('id', 'elezione')
        sezioni = Sezione.objects.prefetch_related('elezione').select_related('elezione').filter(elezione__chiusa=False).all()
    elif user.profilo.is_(Profilo.RILEVATORE):
        # Tutte le sezione a cui è associato
        sezioni = Sezione.objects.filter(rilevatore_id=request.user.id, elezione__chiusa=False).all()
    elif user.profilo.is_(Profilo.RICERCATORE):
        #TODO Tutte le sezione delle elezioni a cui è associato
        #sezioni = Sezione.objects.filter(elezione__=request.user.id, elezione__chiusa=False).all()
        Sezione.objects.filter(elezione__ricercatori__in=[user], elezione__chiusa=False).distinct()
        pass
    elif user.profilo.is_(Profilo.AMMINISTRATORE) or user.is_staff:
        # Tutte le sezioni di tutte le elezioni
        sezioni = Sezione.objects.filter(elezione__chiusa=False).all()

    if sezioni.count() == 1:
        return redirect('rilevazione_index', sezione_id=sezioni.first().id)

    return render(request, 'rilevazione/home.html', {'sezioni': sezioni})
    """

@login_required(login_url='/login/')
def rilevazione_index(request, sezione_id):
    #sezione = get_object_or_404(Sezione.objects.select_related('voticandidato__candidato'), pk=sezione_id)
    sezione = Sezione.objects.select_related('votilista_set__lista').get(pk=sezione_id)
    voti_candidato = VotiCandidato.objects.select_related().filter(sezione_id=sezione_id).all()
    voti_lista = VotiLista.objects.select_related().filter(sezione_id=sezione_id).all()
    return render(request, 'rilevazione/rilevazione.html', {'sezione': sezione, 'voti_candidato': voti_candidato, 'voti_lista': voti_lista})



from django.forms.models import modelform_factory

@login_required(login_url='/login/')
@permission_required('elezioni.can_update_votes','/login/', True)
def edita_sezione(request, sezione_id):
    SezioneForm = modelform_factory(Sezione, fields=("votanti", "iscritti"))
    sezione = get_object_or_404(Sezione, pk=sezione_id)

    if request.method == 'POST':
        form = SezioneForm(request.POST, instance=sezione)
        if form.is_valid():
            form.save()
            return render(request, 'rilevazione/edita_sezione.html', { 'sezione': sezione, 'form': form})
            #return redirect('rilevazione_index', sezione_id=sezione.id)
    else:
        form = SezioneForm(instance=sezione)

    return render(request, 'rilevazione/edita_sezione.html', { 'sezione': sezione, 'form': form})

from django.core import serializers

# ### REPORT
# ### ==================================================

@login_required(login_url='/login/')
@permission_required('elezioni.can_view_reports','/login/', True)
def report_home(request):
    user = request.user

    if user.is_superuser:
        elezioni = Elezione.aperte.all()
    elif is_member_of(user, config.RICERCATORI):
        elezioni = Elezione.aperte.filter(ricercatori__in=[user]).distinct()
    else:
        elezioni = Elezione.aperte.all()

    if elezioni.count() == 1:
        return redirect('report_candidati', elezione_id=elezioni.first().id)
        pass

    return render(request, 'index.html', { 'elezioni': elezioni  })

@login_required(login_url='/login/')
@permission_required('elezioni.can_view_reports','/login/', True)
@transaction.atomic
def crea_proiezione(request, elezione_id):
    elezione = get_object_or_404(Elezione, pk=elezione_id)
    copertura = elezione.get_copertura_campione()
    if copertura > 0:
        p = Proiezione(elezione=elezione, copertura=0).save()
        data = serializers.serialize("json", Proiezione.objects.all())
    #return HttpResponse(data, content_type="application/json")
    #return redirect('report_home')
    return redirect('report_candidati', elezione_id=elezione.id)

@login_required(login_url='/login/')
@permission_required('elezioni.can_view_reports','/login/', True)
@transaction.atomic
def report_candidati(request, elezione_id, ponderati=False):
    elezione = get_object_or_404(Elezione, pk=elezione_id)



    return render(request, 'report/report.html', { 'elezione': elezione, 'risultati': elezione.get_risultati(Candidato, ponderati)})

@login_required(login_url='/login/')
@permission_required('elezioni.can_view_reports','/login/', True)
@transaction.atomic
def report_liste(request, elezione_id, ponderati=False):
    elezione = get_object_or_404(Elezione, pk=elezione_id)

    return render(request, 'report/report.html', { 'elezione': elezione, 'risultati': elezione.get_risultati(Lista, ponderati)})

from django.conf import settings
import time

def aggiorna_voti(request):
    if request.is_ajax():
        if getattr(settings, 'DEBUG', False):
            pass
            #import time
            #import random
            #time.sleep(random.randint(0,4)) # delay AJAX response for 5 seconds

        try:
            id = int(request.POST['vid'])
            tipo = str(request.POST['tipo'])
            if tipo == 'candidato':
                v = get_object_or_404(VotiCandidato, pk=id)
            elif tipo == 'lista':
                v = get_object_or_404(VotiLista, pk=id)
            else:
                raise Http404
            op = str(request.POST['op'])

            voti = v.voti + (1 if op == 'inc' else -1)
            if voti >= 0:
                try:
                    v.ultimo_aggiornamento = datetime.now()
                except:
                    pass
                v.voti = voti
                v.save()
        except KeyError:
            return HttpResponse('Error') # valori errati
        return HttpResponse(v.voti)
    else:
        raise Http404

def test_bianche(request):
    #print request.POST
    if request.is_ajax():
        if getattr(settings, 'DEBUG', False): # only if DEBUG=True
            import time
            import random
            #time.sleep(random.randint(0,4)) # delay AJAX response for 5 seconds
        #print "Ajax"
        try:
            id = int(request.POST['vid'])
            s = get_object_or_404(Sezione, pk=id)
            op = str(request.POST['op'])

            schede_bianche = s.schede_bianche + (1 if op == 'inc' else -1)
            if schede_bianche >= 0:
                s.schede_bianche = schede_bianche
                s.save()
            #board_pk = int(request.POST['board'])
            #moves = list(map(int, request.POST['move_list'].split(',')))
        except KeyError:
            return HttpResponse('Error') # incorrect post
        # do stuff, e.g. calculate a score
        return HttpResponse(s.schede_bianche)
    else:
        raise Http404

def test_nulle(request):
    #print request.POST
    if request.is_ajax():
        if getattr(settings, 'DEBUG', False): # only if DEBUG=True
            import time
            import random
            #time.sleep(random.randint(0,4)) # delay AJAX response for 5 seconds
        #print "Ajax"
        try:
            id = int(request.POST['vid'])
            s = get_object_or_404(Sezione, pk=id)
            op = str(request.POST['op'])

            schede_nulle = s.schede_nulle + (1 if op == 'inc' else -1)
            if schede_nulle >= 0:
                s.schede_nulle = schede_nulle
                s.save()
            #board_pk = int(request.POST['board'])
            #moves = list(map(int, request.POST['move_list'].split(',')))
        except KeyError:
            return HttpResponse('Error') # incorrect post
        # do stuff, e.g. calculate a score
        return HttpResponse(s.schede_nulle)
    else:
        raise Http404

def test2(request):
    #print request.POST
    if request.is_ajax():
        if getattr(settings, 'DEBUG', False): # only if DEBUG=True
            import time
            import random
            #time.sleep(random.randint(0,2)) # delay AJAX response for 5 seconds
        #print "Ajax"
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


def check_proiezione(request):
    #return HttpResponse('True')
    #print request.GET
    if request.is_ajax():
        if getattr(settings, 'DEBUG', False): # only if DEBUG=True
            import time
            import random
            #time.sleep(random.randint(0,2)) # delay AJAX response for 5 seconds
        #print "Ajax"
        try:
            id = int(request.GET['id'])
            #print id
            e = get_object_or_404(Elezione, pk=id)
        except KeyError:
            return HttpResponse('Error') # incorrect post
        # do stuff, e.g. calculate a score
        return HttpResponse(e.proiezioni.last().id)
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

def permission_denied_view(request):
    #return HttpResponse('Permessi insufficienti')
    return render(request, '403.html')