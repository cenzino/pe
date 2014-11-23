from django.conf.urls import patterns, include, url
import views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    #url(r'^(?P<elezione_id>\d+)/$', views.dettaglio, name='dettaglio'),

    url(r'^proiezioni/(?P<elezione_id>\d+)/p/$', views.crea_proiezione, name='crea_proiezione'),

    url(r'^proiezioni/$', views.proiezioni_home, name='proiezioni_home'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/candidati/$', views.proiezioni_candidati, name='proiezioni_candidati'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/liste/$', views.proiezioni_liste, name='proiezioni_liste'),
    #url(r'^proiezioni/(?P<elezione_id>\d+)/candidato/$', views.proiezioni_candidato_one, name='proiezioni_candidato_one'),
    url(r'^proiezioni/(?P<elezione_id>\d+)/candidato/(?P<candidato_id>\d+)/$', views.proiezioni_candidato, name='proiezioni_candidato'),

    url(r'^report/$', views.report_home, name='report_home'),
    url(r'^report/(?P<elezione_id>\d+)/candidati/$', views.report_candidati, {'ponderati': True }, name='report_candidati'),
    url(r'^report/(?P<elezione_id>\d+)/liste/$', views.report_liste, {'ponderati': True }, name='report_liste'),

    url(r'^report/(?P<elezione_id>\d+)/candidati-dati/$', views.report_candidati, name='report_candidati_dati'),
    url(r'^report/(?P<elezione_id>\d+)/liste-dati/$', views.report_liste, name='report_liste_dati'),

    url(r'^rilevazione/$', views.rilevazione_home, name='rilevazione_home'),
    url(r'^rilevazione/(?P<sezione_id>\d+)/$', views.rilevazione_index, name='rilevazione_index'),
    url(r'^rilevazione/(?P<sezione_id>\d+)/edita/$', views.edita_sezione, name='edita_sezione'),


    url(r'^check$', views.check_proiezione, name='check'),
)# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

