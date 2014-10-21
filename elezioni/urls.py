from django.conf.urls import patterns, include, url
import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^(?P<elezione_id>\d+)/$', views.dettaglio, name='dettaglio'),

    url(r'^proiezioni/(?P<elezione_id>\d+)/p/$', views.crea_proiezione, name='crea_proiezione'),

    url(r'^proiezioni/(?P<elezione_id>\d+)/$', RedirectView.as_view(pattern_name='proiezioni_candidati'), name='proiezioni_home'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/candidati/$', views.proiezioni_index, name='proiezioni_candidati'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/candidati2/$', views.proiezioni_candidati2, name='proiezioni_candidati2'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/liste/$', views.proiezioni_liste, name='proiezioni_liste'),

    url(r'^report/(?P<elezione_id>\d+)/$', RedirectView.as_view(pattern_name='report_candidati'), name='report_home'),
    url(r'^report/(?P<elezione_id>\d+)/candidati/$', views.report_candidati, {'ponderati': True }, name='report_candidati'),
    url(r'^report/(?P<elezione_id>\d+)/liste/$', views.report_liste, name='report_liste'),

    url(r'^rilevazione/(?P<sezione_id>\d+)/$', views.rilevazione_index, name='rilevazione_index'),

    url(r'^rilevazione/(?P<sezione_id>\d+)/edita/$', views.edita_sezione, name='edita_sezione'),
    url(r'^rilevazione/(?P<votocandidato_id>\d+)/aumentaC/$', views.aumentaVotoCandidato, name='aumentaVotoCandidato'),
    url(r'^rilevazione/(?P<votocandidato_id>\d+)/diminuisciC/$', views.diminuisciVotoCandidato, name='diminuisciVotoCandidato'),
    url(r'^rilevazione/(?P<votolista_id>\d+)/aumentaL/$', views.aumentaVotoLista, name='aumentaVotoLista'),
    url(r'^rilevazione/(?P<votolista_id>\d+)/diminuisciL/$', views.diminuisciVotoLista, name='diminuisciVotoLista'),
)# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

