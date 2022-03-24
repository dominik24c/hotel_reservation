from base.models import BaseModelWithDateTime
from django.contrib.auth.models import User
from django.db import models
from hotel.models import Room


# Create your models here.


class Reservation(BaseModelWithDateTime):
    customer = models.ForeignKey(to=User, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, related_name='reservation', on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
