import uuid

from account.models import HotelOwner, Customer
from base.test import BaseApiTestCase
from django.urls import reverse
from django.utils import timezone
from hotel.models import Room
from hotel.tests.factory import create_hotels, create_rooms
from rest_framework import status

from .factory import create_reservations
from ..models import Reservation


class ReservationApiViewTest(BaseApiTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        users = list(Customer.objects.all())
        hotels = create_hotels(list(HotelOwner.objects.all()))
        rooms = create_rooms(hotels, 7)
        create_reservations(rooms, users)

    def setUp(self) -> None:
        self.user = Customer.objects.prefetch_related('reservations').first()
        self.client.force_authenticate(self.user)

    def _testcase_for_get_routes(self, data: dict, reservation: Reservation) -> None:
        self.assertEqual(data['start_date'], reservation.start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data['end_date'], reservation.end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(data['room'], str(reservation.room.id))

    def _test_invalid_create_reservation_view(self, body: dict, message: str):
        response = self.client.post(reverse('reservation:reservation-list'), body)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        if isinstance(response.data, dict):
            self.assertEqual(response.data['non_field_errors'][0], message)
        elif isinstance(response.data, list):
            self.assertEqual(response.data[0], message)

    def test_list_reservation_view(self) -> None:
        response = self.client.get(reverse('reservation:reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['results']
        self.assertEqual(len(data), self.user.reservations.count())
        for res, reservation in zip(data, self.user.reservations.all()):
            self._testcase_for_get_routes(res, reservation)

    def test_create_reservation_view(self) -> None:
        room = Room.objects.first()
        amount_of_reservations = self.user.reservations.count()
        body = {
            'room': str(room.id),
            'start_date': str(timezone.datetime(2027, 1, 4)),
            'end_date': str(timezone.datetime(2027, 2, 10)),
        }
        response = self.client.post(reverse('reservation:reservation-list'), body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user.refresh_from_db()
        self.assertEqual(amount_of_reservations + 1, self.user.reservations.count())

    def test_create_reservation_view_with_invalid_room_id(self) -> None:
        body = {
            'room': str(uuid.uuid4()),
            'start_date': str(timezone.datetime(2021, 2, 4)),
            'end_date': str(timezone.datetime(2021, 2, 10)),
        }
        self._test_invalid_create_reservation_view(body, "Room doesn't exists!")

    def test_create_reservation_view_with_invalid_dates(self) -> None:
        room = Room.objects.first()
        body = {
            'room': str(room.id),
            'start_date': str(timezone.datetime(2021, 2, 14)),
            'end_date': str(timezone.datetime(2021, 2, 10)),
        }
        self._test_invalid_create_reservation_view(body, "The end date must be greater than start date!")

    def test_create_reservation_view_with_unavailable_room(self) -> None:
        start_date = timezone.datetime(2021, 2, 9).replace(tzinfo=timezone.utc)
        end_date = timezone.datetime(2021, 2, 12).replace(tzinfo=timezone.utc)
        room = Room.objects.first()
        Reservation.objects.create(customer=self.user, room=room, start_date=start_date, end_date=end_date)
        body = {
            'room': str(room.id),
            'start_date': str(timezone.datetime(2021, 2, 9)),
            'end_date': str(timezone.datetime(2021, 2, 12)),
        }

        start_dates = [str(date) for date in
                       [timezone.datetime(2021, 2, 9), timezone.datetime(2021, 2, 8), timezone.datetime(2021, 2, 11)]]
        end_dates = [str(date) for date in
                     [timezone.datetime(2021, 2, 12), timezone.datetime(2021, 2, 11), timezone.datetime(2021, 2, 15)]]

        for start_date, end_date in zip(start_dates, end_dates):
            body['start_date'] = start_date
            body['end_date'] = end_date
            self._test_invalid_create_reservation_view(body, "Room is not available! Choose other date.")

    def test_detail_reservation_view(self) -> None:
        reservation = self.user.reservations.first()
        response = self.client.get(reverse('reservation:reservation-detail', kwargs={'pk': str(reservation.id)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._testcase_for_get_routes(response.data, reservation)

    def test_delete_reservation_view(self) -> None:
        reservation = self.user.reservations.first()
        response = self.client.delete(reverse('reservation:reservation-detail', kwargs={'pk': str(reservation.id)}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Reservation.DoesNotExist):
            reservation.refresh_from_db()

    def test_update_reservation_view(self) -> None:
        reservation = self.user.reservations.first()
        body = {
            'start_date': str(timezone.datetime(2022, 5, 9)),
            'end_date': str(timezone.datetime(2022, 5, 12)),
        }
        response = self.client.put(reverse('reservation:reservation-detail', kwargs={'pk': str(reservation.id)}), body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

