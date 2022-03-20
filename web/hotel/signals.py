from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Hotel


@receiver(pre_save, sender=Hotel)
def pre_save_hotel_handler(instance, sender, *args, **kwargs) -> None:
    instance.country = instance.country.lower()
    instance.city = instance.city.lower()
    instance.street = instance.street.lower()
