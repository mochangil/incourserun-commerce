from app.order.models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Social
from ..cart.models import Cart


@receiver(post_save, sender=User)
def on_change(sender, update_fields, created, instance, **kwargs):
    if not created and not instance.is_active:
        Cart.objects.filter(user=instance).delete()
        Order.objects.filter(user=instance).delete()
        Social.objects.filter(user=instance).delete()
    if created:
        pass
