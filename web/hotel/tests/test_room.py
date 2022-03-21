from account.models import HotelOwner
from base.test import BaseApiTestCase
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from .factory import create_hotels, create_rooms
from ..models import Room, Hotel


class RoomApiViewTest(BaseApiTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        hotels = create_hotels(list(HotelOwner.objects.all()))
        create_rooms(hotels, 7)

    def setUp(self) -> None:
        self.hotel_owner = HotelOwner.objects.prefetch_related('hotels__rooms').first()
        self.client.force_authenticate(self.hotel_owner)

    def _test_response_data(self, data: dict, room: Room) -> None:
        self.assertEqual(data['number'], room.number)
        self.assertEqual(data['size'], room.size)
        self.assertEqual(data['price'], str(room.price))
        self.assertEqual(data['beds'], room.beds)
        self.assertEqual(data['is_tv'], room.is_tv)
        self.assertEqual(data['is_shower'], room.is_shower)
        self.assertEqual(data['is_toilet'], room.is_toilet)

    def _get_room(self) -> Room:
        return self.hotel_owner.hotels.first().rooms.first()

    def test_list_room_view(self) -> None:
        response = self.client.get(reverse('hotel:create-list-room-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), settings.REST_FRAMEWORK['PAGE_SIZE'])
        rooms = list(Room.objects.prefetch_related('hotel').all()[:10])
        for data, room in zip(response.data['results'], rooms):
            self.assertEqual(data['id'], str(room.id))
            self.assertEqual(data['hotel_id'], str(room.hotel.id))
            self._test_response_data(data, room)

    def test_create_room_view(self) -> None:
        hotel = Hotel.objects.prefetch_related('rooms').first()
        body = {
            'hotel_id': hotel.id,
            'number': 100,
            'size': 120,
            'price': '400.32',
            'beds': 4,
            'is_tv': True,
            'is_shower': False,
            'is_toilet': True,
        }

        response = self.client.post(reverse('hotel:create-list-room-view'), body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Room was created!')
        hotel.refresh_from_db()
        room = hotel.rooms.first()
        self._test_response_data(body, room)

    def test_delete_room_view(self) -> None:
        room = self._get_room()
        response = self.client.delete(reverse('hotel:rud-room-view', kwargs={'pk': room.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Room.DoesNotExist):
            room.refresh_from_db()

    def test_retrieve_room_view(self) -> None:
        room = self._get_room()
        response = self.client.get(reverse('hotel:rud-room-view', kwargs={'pk': room.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._test_response_data(response.data, room)

    def test_update_room_view(self) -> None:
        room = self._get_room()
        body = {
            'number': 99,
            'size': 210,
            'price': '193.21',
            'beds': 2,
            'is_tv': True,
            'is_shower': False,
            'is_toilet': True,
        }

        response = self.client.put(reverse('hotel:rud-room-view', kwargs={'pk': room.id}), body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        room.refresh_from_db()
        self._test_response_data(body, room)
