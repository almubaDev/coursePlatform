from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

# Aquí puedes agregar señales relacionadas con el usuario
# Por ejemplo, si necesitas crear automáticamente un perfil adicional
# o enviar un correo de bienvenida cuando se crea un usuario

# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Crea un perfil automáticamente cuando se crea un usuario."""
#     if created:
#         # Ejemplo: Profile.objects.create(user=instance)
#         pass