import random

import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger, FuzzyDecimal

from ..models import Hotel, Room


class HotelFactory(DjangoModelFactory):
    class Meta:
        model = Hotel

    name = factory.Sequence(lambda n: f'Hotel{n}')
    description = factory.Faker('text')
    country = factory.Faker('country')
    city = factory.Faker('city')
    street = factory.Sequence(lambda n: f'Wall street {n}')
    zip_code = factory.Sequence(lambda n: f'58-3{n}9')


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    number = factory.Sequence(lambda n: n)
    beds = FuzzyInteger(1, 4)
    size = FuzzyInteger(25, 120)
    price = FuzzyDecimal(150.0, 700.0)
    is_shower = factory.Sequence(lambda _: bool(random.randrange(0, 2)))
    is_tv = factory.Sequence(lambda _: bool(random.randrange(0, 2)))
    is_toilet = factory.Sequence(lambda _: bool(random.randrange(0, 2)))


def create_hotels(users: list[User]) -> list[Hotel]:
    hotels = [HotelFactory.build(owner=user) for user in users]
    Hotel.objects.bulk_create(hotels)
    return hotels


def create_rooms(hotels: list[Hotel], amount_of_rooms) -> list[Room]:
    rooms = []
    for hotel in hotels:
        tmp_rooms = [RoomFactory.build(hotel=hotel) for _ in range(amount_of_rooms)]
        Room.objects.bulk_create(tmp_rooms)
        rooms.extend(tmp_rooms)

    return rooms
