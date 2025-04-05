from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import EssayAttempt, TestCoupon


@receiver(pre_save, sender=EssayAttempt)
def update_analysis_date(sender, instance, **kwargs):
    """Actualiza la fecha de análisis cuando el estado cambia a 'analyzed'."""
    try:
        # Si el objeto ya existe, obtenemos la instancia anterior
        old_instance = EssayAttempt.objects.get(pk=instance.pk)
        # Si el estado ha cambiado a 'analyzed', actualizamos la fecha
        if old_instance.status != 'analyzed' and instance.status == 'analyzed':
            instance.date_analyzed = timezone.now()
    except EssayAttempt.DoesNotExist:
        # Es un nuevo objeto, no hacemos nada
        pass


@receiver(pre_save, sender=TestCoupon)
def update_coupon_used_date(sender, instance, **kwargs):
    """Actualiza la fecha de uso cuando el cupón es marcado como usado."""
    try:
        old_instance = TestCoupon.objects.get(pk=instance.pk)
        if not old_instance.is_used and instance.is_used:
            instance.used_date = timezone.now()
    except TestCoupon.DoesNotExist:
        # Es un nuevo cupón
        pass