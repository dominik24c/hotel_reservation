from datetime import datetime

from base.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from hotel.models import Room


class ReservationManager(models.Manager):
    def room_is_available(self, room_id: str, start_date: datetime, end_date: datetime, reservation_id: str = None) -> bool:
        filters = Q(room__id=room_id) & ~(
                (Q(start_date__gt=start_date) & Q(start_date__gt=end_date)) |
                (Q(end_date__lt=start_date) & Q(end_date__lt=end_date)))

        if reservation_id is not None:
            filters = filters & ~Q(id=reservation_id)

        if Reservation.objects.filter(filters).exists():
            return False
        return True


class Reservation(TimeStampedModel):
    customer = models.ForeignKey(to=User, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    objects = ReservationManager()

    class Meta:
        ordering = ['-updated_at']
