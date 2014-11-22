from django.contrib import admin
from .models import *
from django.core import urlresolvers
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.db import transaction

from django.utils.translation import ugettext_lazy as _
import config

"""
class ProfiloInline(admin.StackedInline):
    model = Profilo
    can_delete = False
    verbose_name_plural = 'Profilo utente'
"""

def make_active(modeladmin, request, queryset):
    queryset.filter(is_superuser=False).update(is_active=True)
make_active.short_description = "Attiva utenti selezioni/e"

def make_inactive(modeladmin, request, queryset):
    queryset.filter(is_superuser=False).update(is_active=False)
make_inactive.short_description = "Disattiva utenti selezioni/e"

class InfoUtenteInline(admin.StackedInline):
    model = InfoUtente
    can_delete = False
    verbose_name_plural = 'Informazioni Utenti'

class UserAdmin(UserAdmin):
    list_display = ('username', 'id', 'full_name', 'is_ricercatore', 'is_rilevatore', 'is_emittente', 'is_staff', 'is_active', 'is_superuser')
    list_select_related = True
    #inlines = (ProfiloInline, )
    list_filter = ('is_staff',)

    save_on_top = True

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'classes': ('collapse', ),
            'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Gruppi'), {
            'classes': ('collapse', ),
            'fields': ('groups', )}),
        ('Permessi Avanzati', {
            'classes': ('collapse', ),
            'fields': ('user_permissions', )
        }),
        #(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    inlines = (InfoUtenteInline, )

    def is_ricercatore(self, obj):
        try:
            return config.RICERCATORI in [g['name'] for g in obj.groups.values()]
        except:
            return False
    is_ricercatore.short_description = 'Ricercatore'
    is_ricercatore.boolean = True

    def is_rilevatore(self, obj):
        try:
            return config.RILEVATORI in [g['name'] for g in obj.groups.values()]
        except:
            return False
    is_rilevatore.short_description = 'Rilevatore'
    is_rilevatore.boolean = True

    def is_emittente(self, obj):
        try:
            return config.EMITTENTI in [g['name'] for g in obj.groups.values()]
        except:
            return False
    is_emittente.short_description = 'Emittente'
    is_emittente.boolean = True


    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = "Nome completo"

    list_filter += ('is_active', 'groups', )

    actions = [make_active, make_inactive]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class GroupAdmin(GroupAdmin):
    list_display = ('name', 'utenti', 'is_sistem_group' )
    filter_horizontal = ('permissions',)

    def is_sistem_group(self, obj):
        return obj.name in config.DEFAULT_SYSTEM_GROUPS
    is_sistem_group.short_description = "Gruppo di sistema (non cancellabile)"
    is_sistem_group.boolean = True

    def utenti(self, obj):
        return User.objects.filter(groups__in=[obj,]).count()
    utenti.short_description = "Numero utenti"

    def get_actions(self, request):
        #Disable delete
        actions = super(GroupAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if obj.name in config.DEFAULT_SYSTEM_GROUPS:
            #print dir(obj)
            readonly_fields.extend(['name','permissions'])
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        try:
            if obj.name in config.DEFAULT_SYSTEM_GROUPS:
                return False
        except:
            return False
        return True

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)


class SezioneInline(admin.TabularInline):
    model = Sezione
    extra = 0
    exclude = ['luogo',]

class ListaInline(admin.TabularInline):
    model = Lista
    extra = 0


class CandidatoInline(admin.TabularInline):
    model = Candidato
    fields = ('cognome', 'nome', 'foto', 'admin_url')
    readonly_fields = ('admin_url',)
    extra = 0

    def admin_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_admin_url(), 'Liste')

    admin_url.allow_tags = True
    admin_url.short_description = 'Edita'

"""
class EmittenteInline(admin.TabularInline):
    model = EmittenteElezione
    extra = 0
"""


@admin.register(Elezione)
class ElezioneAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'chiusa')
    fieldsets = (
        (None, {
            'fields': (('titolo', 'descrizione'), 'chiusa', 'aventi_diritto', 'copertura_simulata')}),
        ('Ricercatori', {
            'classes': (),
            'fields': ('ricercatori', 'emittenti')
        }),
    )
    inlines = [
        #EmittenteInline,
        CandidatoInline,
        SezioneInline,
        #ListaInline
    ]

    #filter_horizontal = ('ricercatori', )

    class Media:
        css = {
            "all": ("admin.css",)
        }

#@admin.register(VotiCandidato)
class VotiCandidatoAdmin(admin.ModelAdmin):
    list_display = ('sezione','candidato','voti','updated_at')
    readonly_fields=('sezione','candidato',)
    list_filter = ('candidato',)
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False


#admin.site.register(VotiLista)

class VotiCandidatoInline(admin.TabularInline):
    list_display = ('id','sezione','candidato','voti')
    readonly_fields=('sezione','candidato', 'ultimo_aggiornamento', )
    fields = (('candidato', 'voti', 'ultimo_aggiornamento',),)
    model = VotiCandidato
    extra = 0
    list_filter = ('candidato',)

    ordering = ['id',]

    actions = None
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False

class VotiListaInline(admin.TabularInline):
    list_display = ('sezione','lista','voti')
    readonly_fields=('sezione','lista', 'ultimo_aggiornamento', )
    fields = ('lista', 'voti', 'ultimo_aggiornamento',)
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


class DatiProiezioneCandidatoInline(admin.TabularInline):
    model = DatiProiezioneCandidato
    fields = ('candidato', 'voti','forbice', 'voti_liste', 'forbice_liste',)
    list_display = ['candidato','voti',]
    readonly_fields=('candidato',)
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False

    ordering = ['id',]


    class Media:
        css = {
            "all": ("admin.css",)
        }

class DatiProiezioneListaInline(admin.TabularInline):
    model = DatiProiezioneLista
    fields = ('lista', 'voti', 'forbice')
    #list_display = ['candidato','voti',]
    readonly_fields=('lista',)
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False

    class Media:
        css = {
            "all": ("admin.css",)
        }

@admin.register(Proiezione)
class ProiezioneAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'elezione', '_get_copertura', 'data_creazione', 'pubblicata','generata_da_riserve')
    readonly_fields=('elezione',)

    inlines = [
        DatiProiezioneCandidatoInline,
        DatiProiezioneListaInline
    ]

    list_filter = ('elezione',)

    def _get_copertura(self, obj):
        return "%s %%" % (round(obj.copertura*100,1))
    _get_copertura.short_description = "Copertura campione"


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_filter = ('elezione',)