from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ProiezioniElezioni.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'elezioni.views.home', name='home'),
    url(r'^elezioni/', include('elezioni.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login',  {'template_name': '_login.html'},name='login', ),
    url(r'^logout/$', 'django.contrib.auth.views.logout',  {'template_name': 'bye.html'}, name='logout',),

) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )