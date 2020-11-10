from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    name = 'apps.core'
    label = 'core'
    verbose_name = _('Core')

    def ready(self):
        from apps.core import signals
