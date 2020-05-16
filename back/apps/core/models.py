from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from libs.cryptography import hashing
from libs.helpers.datetimepresets import day_later


class PersonRegistrationRequest(models.Model):
    email = models.EmailField(verbose_name=_('Email'),
                              max_length=128)

    url = models.CharField(verbose_name=_('URL Prefix'),
                           max_length=64)

    key = models.CharField(verbose_name=_('Registration key'),
                           editable=False,
                           max_length=128)

    created_at = models.DateTimeField(verbose_name=_('Created at'),
                                      auto_now_add=True)

    expired_at = models.DateTimeField(verbose_name=_('Expired at'),
                                      default=day_later)

    class Meta:
        db_table = 'core_person_registration_request'
        ordering = ['-expired_at']
        verbose_name = _('Person Registrations Request')
        verbose_name_plural = _('Person Registrations Requests')

    def __str__(self):
        return f'{self.email} - {self.url}'

    __repr__ = __str__

    def save(self, *args, **kwargs):
        if self.pk is None:
            raw_string = ''.join([str(self.expired_at), self.email, self.url])
            self.key = hashing.get_hash(raw_string)

        super(PersonRegistrationRequest, self).save(self, *args, **kwargs)


class Person(models.Model):
    """
    Person should be connected to user.
    Person can be invited, but have to fill of this information by himself
    """

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
    def username(self):
        return self.user.username

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
        return f'{self.first_name or _("Unnamed") } {self.last_name}'

    __repr__ = __str__
