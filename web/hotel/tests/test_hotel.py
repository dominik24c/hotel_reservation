from account.models import HotelOwner
from base.test import BaseApiTestCase
from django.urls import reverse
from rest_framework import status

from .factory import create_hotels, create_rooms
from ..models import Hotel


class BaseHotelApiViewTestCase(BaseApiTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        hotels = create_hotels(list(HotelOwner.objects.all()))
        create_rooms(hotels, 7)

    def _base_hotel_test_case(self, data: dict, hotel: Hotel) -> None:
        self.assertEqual(data['name'], hotel.name)
        self.assertEqual(data['owner'], hotel.owner.username)
        self.assertEqual(data['description'], hotel.description)
        self.assertEqual(data['is_wifi'], hotel.is_wifi)
        self.assertEqual(data['is_pools'], hotel.is_pools)


class HotelApiViewTest(BaseHotelApiViewTestCase):

    def test_create_hotel_view(self) -> None:
        hotel_owner = HotelOwner.objects.prefetch_related('hotels').first()
        body = {
            'name': 'The Plaza Hotel',
            'owner': hotel_owner.username,
            'is_wifi': True,
            'is_pools': True,
            'description': 'its famous hotel for rich persons.',
            'country': 'uSa',
            'city': 'New york',
            'street': 'Wall Street 1',
            'zip_code': '10019'
        }

        response = self.client.post(reverse('hotel:create-hotel-view'), body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        hotel_owner.refresh_from_db()
        hotel = hotel_owner.hotels.filter(name=body['name']).first()

        data = response.data
        self._base_hotel_test_case(body, hotel)
        self.assertEqual(body['country'].lower(), hotel.country)
        self.assertEqual(body['city'].lower(), hotel.city)
        self.assertEqual(body['street'].lower(), hotel.street)
        self.assertEqual(body['zip_code'], hotel.zip_code)
        self.assertEqual(data['message'], 'Hotel was created!')

    def test_list_hotel_view(self) -> None:
        response = self.client.get(reverse('hotel:hotel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(data), Hotel.objects.count() % 10)


class HotelRUDApiViewTest(BaseHotelApiViewTestCase):

    def setUp(self) -> None:
        self.client.force_authenticate(HotelOwner.objects.first())

    def test_retrieve_hotel_view(self) -> None:
        hotel = Hotel.objects.prefetch_related('owner').first()
        response = self.client.get(reverse('hotel:hotel-detail', kwargs={'pk': hotel.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self._base_hotel_test_case(data, hotel)
        self.assertEqual(data['address'], hotel.full_address)
        self.assertEqual(data['country'], hotel.country)

    def test_delete_hotel_view(self) -> None:
        hotel_owner = HotelOwner.objects.prefetch_related('hotels').first()
        hotel = hotel_owner.hotels.first()
        response = self.client.delete(reverse('hotel:update-delete-hotel-view', kwargs={'pk': hotel.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Hotel.DoesNotExist):
            hotel.refresh_from_db()

    def test_update_hotel_view(self) -> None:
        hotel_owner = HotelOwner.objects.prefetch_related('hotels').first()
        hotel = hotel_owner.hotels.first()
        body = {
            'description': 'New description',
            'name': 'new hotel'
        }
        response = self.client.put(reverse('hotel:update-delete-hotel-view', kwargs={'pk': hotel.pk}), body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], body['name'])
        self.assertEqual(response.data['description'], body['description'])
