from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Profile


@receiver(pre_save, sender=Profile)
def pre_save_profile(instance, sender, *args, **kwargs) -> None:
    instance.country = instance.country.lower()
