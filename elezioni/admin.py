from django.contrib import admin
from .models import *
# Register your models here.

#admin.site.register(Elezione)
#admin.site.register(Sezione)

class SezioneInline(admin.TabularInline):
    model = Sezione
    extra = 0

class ListaInline(admin.TabularInline):
    model = Lista
    extra = 0


class CandidatoInline(admin.TabularInline):
    model = Candidato
    fields = ('cognome', 'nome', 'foto')
    #list_display = ('cognome', 'nome')
    extra = 0

@admin.register(Elezione)
class ElezioneAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('titolo', 'descrizione'), 'chiusa', 'aventi_diritto', 'copertura_simulata')
        }),
    )
    inlines = [
        CandidatoInline,
        SezioneInline,
        #ListaInline
    ]

    class Media:
        css = {
            "all": ("admin.css",)
        }

@admin.register(VotiCandidato)
class VotiCandidatoAdmin(admin.ModelAdmin):
    list_display = ('sezione','candidato','voti')
    readonly_fields=('sezione','candidato',)
    list_filter = ('candidato',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False


admin.site.register(VotiLista)

class VotiCandidatoInline(admin.TabularInline):
    list_display = ('sezione','candidato','voti')
    readonly_fields=('sezione','candidato',)
    fields = (('candidato', 'voti',),)
    model = VotiCandidato
    extra = 0
    list_filter = ('candidato',)

    actions = None
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False

class VotiListaInline(admin.TabularInline):
    list_display = ('sezione','lista','voti')
    readonly_fields=('sezione','lista',)
    fields = ('lista', 'voti',)
    model = VotiLista
    extra = 0

    actions = None
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False

@admin.register(Sezione)
class SezioneAdmin(admin.ModelAdmin):
    list_filter = ('elezione',)
    inlines = [
        VotiCandidatoInline,
        VotiListaInline
    ]

    class Media:
        css = {
            "all": ("admin.css",)
        }


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('cognome', 'nome'), 'foto')
        }),
    )
    list_filter = ('elezione',)
    inlines = [
        ListaInline,
    ]