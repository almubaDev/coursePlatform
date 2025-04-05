from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = _('Usuarios')

    def ready(self):
        import users.signals  # Importar señales si se llegan a necesitar