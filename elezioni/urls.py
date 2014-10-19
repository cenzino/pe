from django.conf.urls import patterns, include, url
import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^(?P<elezione_id>\d+)/$', views.dettaglio, name='dettaglio'),

    url(r'^proiezioni/(?P<elezione_id>\d+)/$', views.proiezioni_index, name='proiezioni_index'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/candidati/$', views.proiezioni_index, name='proiezioni_index'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/candidati2/$', views.proiezioni_candidati2, name='proiezioni_candidati2'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/liste/$', views.proiezioni_liste, name='proiezioni_liste'),

    url(r'^report/(?P<elezione_id>\d+)/candidati/$', views.report_candidati_dati_ponderati, name='report_index'),
    url(r'^report/(?P<elezione_id>\d+)/candidati/$', views.report_candidati_dati_ponderati, name='report_candidati_dati_ponderati'),
    url(r'^report/(?P<elezione_id>\d+)/candidati/dati-grezzi$', views.report_candidati_dati_grezzi, name='report_candidati_dati_grezzi'),
    url(r'^report/(?P<elezione_id>\d+)/liste/$', views.report_liste_dati_ponderati, name='report_liste_dati_ponderati'),
    url(r'^report/(?P<elezione_id>\d+)/liste/dati-grezzi$', views.report_liste_dati_grezzi, name='report_liste_dati_grezzi'),
    url(r'^report/(?P<elezione_id>\d+)/test/$', views.report_test, name='report_test'),
    url(r'^report/(?P<elezione_id>\d+)/test-liste/$', views.report_test_liste, name='report_test_liste'),

    url(r'^report/(?P<elezione_id>\d+)/test3/$', views.report_test3, name='report_test3'),
    url(r'^report/(?P<elezione_id>\d+)/test/z/$', views.z, name='report_z'),

    url(r'^rilevazione/(?P<sezione_id>\d+)/$', views.rilevazione_index, name='rilevazione_index'),

    url(r'^rilevazione/(?P<sezione_id>\d+)/edita/$', views.edita_sezione, name='edita_sezione'),
    url(r'^rilevazione/(?P<votocandidato_id>\d+)/aumentaC/$', views.aumentaVotoCandidato, name='aumentaVotoCandidato'),
    url(r'^rilevazione/(?P<votocandidato_id>\d+)/diminuisciC/$', views.diminuisciVotoCandidato, name='diminuisciVotoCandidato'),
    url(r'^rilevazione/(?P<votolista_id>\d+)/aumentaL/$', views.aumentaVotoLista, name='aumentaVotoLista'),
    url(r'^rilevazione/(?P<votolista_id>\d+)/diminuisciL/$', views.diminuisciVotoLista, name='diminuisciVotoLista'),
)# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

