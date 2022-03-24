from datetime import datetime

from django.contrib.auth.models import User
from django.utils.timezone import utc
from factory.django import DjangoModelFactory
from hotel.models import Room

from ..models import Reservation


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation


def create_reservations(rooms: list[Room], users: list[User]) -> list[Reservation]:
    reservations = [
        ReservationFactory.build(customer=user, room=room,
                                 start_date=datetime(2020, 1, 10).utcnow().replace(tzinfo=utc),
                                 end_date=datetime(2020, 1, 18).utcnow().replace(tzinfo=utc))
        for user, room in zip(users, rooms)]
    Reservation.objects.bulk_create(reservations)
    return reservations
