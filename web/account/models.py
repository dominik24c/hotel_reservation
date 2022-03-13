from base_models.models import BaseModel
from django.contrib.auth.models import User
from django.db import models

from . import groups
from .validators import only_letters


class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name=groups.G_CUSTOMER)


class HotelOwnerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name=groups.G_HOTEL_OWNER)


class Profile(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=150, validators=[only_letters])
    date_of_birth = models.DateField()


class Customer(User):
    objects = CustomerManager()

    class Meta:
        proxy = True


class HotelOwner(User):
    objects = HotelOwnerManager()

    class Meta:
        proxy = True
