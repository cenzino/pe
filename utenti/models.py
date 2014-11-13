from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

class BaseUtenteManager(BaseUserManager):

    def create_user(self, username=None, password=None, **extra_fields):
        now = timezone.now()
        u = Utente(
            username=username,
            last_login=now,
            **extra_fields)
        u.set_password(password)
        u.save(using=self._db)
        return u

    def create_superuser(self, username, password, **extra_fields):
        u = self.create_user(
            username=username,
            password=password,
            **extra_fields)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

class BaseUtente(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)

    tipo = models.CharField(max_length=15, editable=False)
    is_superuser = False

    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    objects = BaseUtenteManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new or self.tipo != self.__class__.__name__:
            self.tipo = self.__class__.__name__
        super(BaseUtente, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    get_full_name.short_description = "Nome completo"

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.username


class Utente(BaseUtente):
    objects = BaseUtenteManager()

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'
        permissions = (("proiezioni", "Puo accedere alle proiezioni"),
                       ("report", "Puo accedere ai report"),
                       ("rilevazione", "Puo accedere alla rilevazione"),
        )

class Rilevatore(BaseUtente):
    is_staff = False
    is_superuser = False
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Il numero di telefono deve essere in questo formato: '+1234567890'. Fino a un massimo di 15 cifre.")
    telefono = models.CharField(validators=[telefono_regex,], max_length=15)

    #objects = BaseUtenteManager()

    class Meta:
        verbose_name = 'Rilevatore'
        verbose_name_plural = 'Rilevatori'
        permissions = (("rilevazione", "Puo accedere alla rilevazione"),)

from elezioni.models import Elezione

class Ricercatore(BaseUtente):
    elezioni = models.ManyToManyField(Elezione, related_name='ricercatori', related_query_name='ricercatore', null=True, blank=True)

    is_staff = False
    is_superuser = False

    class Meta:
        verbose_name = 'Ricercatore'
        verbose_name_plural = 'Ricercatori'
        permissions = (("proiezioni", "Puo accedere alle proiezioni"),
                       ("report", "Puo accedere ai report"),
        )

class Emittente(BaseUtente):
    elezioni = models.ManyToManyField(Elezione, through='EmittenteElezione', related_name="emittenti", related_query_name="emittente")
    is_staff = True
    is_superuser = False

    class Meta:
        verbose_name = 'Emittente'
        verbose_name_plural = 'Emittenti'
        permissions = (("proiezioni", "Puo accedere alle proiezioni"),)

from elezioni.models import Elezione, get_image_path
class EmittenteElezione(models.Model):
    from utenti.models import Emittente
    emittente = models.ForeignKey(Emittente)
    elezione = models.ForeignKey(Elezione)
    immagine = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = "EmittentiElezioni"