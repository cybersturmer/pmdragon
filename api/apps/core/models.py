from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from libs.cryptography import hashing
from libs.helpers.datetimepresets import day_later


class PersonRegistrationRequestValidManager(models.Manager):
    def get_queryset(self):
        return super(PersonRegistrationRequestValidManager, self).\
            get_queryset().\
            filter(expired_at__gt=timezone.now())


class PersonRegistrationRequest(models.Model):
    objects = models.Manager()
    valid = PersonRegistrationRequestValidManager()

    url_validator = RegexValidator(r'^[a-z]{3,20}$',
                                   _('String should contain from 3 to 20 small english letters '
                                     'without special chars'))

    email = models.EmailField(verbose_name=_('Email'),
                              max_length=128)

    prefix_url = models.CharField(verbose_name=_('Prefix URL'),
                                  help_text=_('String should contain from 3 to 20 small english letters '
                                              'without special chars'),
                                  validators=[url_validator],
                                  max_length=20)

    key = models.CharField(verbose_name=_('Registration key'),
                           editable=False,
                           max_length=128)

    email_sent = models.BooleanField(verbose_name=_('Registration mail was successfully sent'),
                                     default=False)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    expired_at = models.DateTimeField(verbose_name=_('Expired at'),
                                      default=day_later)

    class Meta:
        db_table = 'core_person_registration_request'
        ordering = ['-expired_at']

        indexes = (
            models.Index(fields=['key']),
            models.Index(fields=['key', '-expired_at'])
        )

        verbose_name = _('Person Registrations Request')
        verbose_name_plural = _('Person Registrations Requests')

    def __str__(self):
        return f'{self.email} - {self.prefix_url}'

    __repr__ = __str__

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):

        if self.pk is None:
            raw_string = ''.join([str(self.expired_at), self.email, self.prefix_url])
            self.key = hashing.get_hash(raw_string)

        super(PersonRegistrationRequest, self).save(force_insert,
                                                    force_update,
                                                    using,
                                                    update_fields)


class Person(models.Model):
    """
    Person should be connected to user.
    Person can be invited, but have to fill of this information by himself
    """

    username = models.CharField(max_length=20,
                                verbose_name=_('Username'),
                                default='dragon')

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name=_('User of system'),
                                on_delete=models.CASCADE)

    phone = models.CharField(max_length=128,
                             verbose_name=_('Phone number'),
                             null=True,
                             blank=True)

    updated_at = models.DateTimeField(verbose_name=_('Updated at'),
                                      auto_now=True)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def created_at(self):
        return self.user.date_joined

    class Meta:
        db_table = 'core_person'
        ordering = ['-updated_at']
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return f'{self.username} - {self.first_name or _("Unnamed")}'

    __repr__ = __str__


