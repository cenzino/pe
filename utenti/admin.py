from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from utenti.models import BaseUtente, Utente, Rilevatore, Emittente, Ricercatore, EmittenteElezione


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = BaseUtente
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            BaseUtente._default_manager.get(username=username)
        except BaseUtente.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = BaseUtente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class BaseUtenteAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'get_full_name', 'tipo','is_staff', 'is_superuser', 'is_active', 'last_login',)
    list_filter = ('is_staff','tipo')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_staff', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide','extrapretty',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)

class UtenteAdmin(BaseUtenteAdmin):
    list_display = ('username', 'get_full_name', 'tipo','is_staff', 'is_superuser', 'is_active', 'last_login',)
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'user_permissions',)}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide','extrapretty',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)

class RicercatoreAdmin(BaseUtenteAdmin):
    list_display = ('username', 'get_full_name', 'is_active', 'last_login',)
    exclude = ('tipo',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (('first_name', 'last_name', 'email'),)}),
        #('Permissions', {'fields': ('is_staff',)}),
        #('Permissions', {'fields': ('is_staff',)}),
        ('Elezioni', {'fields': ('elezioni',)}),
    )
    filter_horizontal = ('elezioni',)


class RilevatoreAdmin(BaseUtenteAdmin):
    list_display = ('username', 'get_full_name', 'telefono', 'is_active', 'last_login',)
    exclude = ('tipo',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'telefono')}),
        #('Permissions', {'fields': ('is_staff',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )

class ElezioniInline(admin.TabularInline):
    model = EmittenteElezione
    extra = 1


class EmittenteAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'is_active', 'last_login',)
    exclude = ('tipo',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'email')}),
        #('Permissions', {'fields': ('is_staff',)}),
    )
    inlines = (ElezioniInline, )
    search_fields = ('username', 'first_name',)

# Now register the new UserAdmin...
admin.site.register(BaseUtente, BaseUtenteAdmin)
admin.site.register(Utente, UtenteAdmin)
admin.site.register(Rilevatore, RilevatoreAdmin)
admin.site.register(Ricercatore, RicercatoreAdmin)
admin.site.register(Emittente, EmittenteAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)