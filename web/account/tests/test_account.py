from base.test import BaseApiTestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from .factory import TEST_PASSWORD
from ..groups import G_CUSTOMER
from ..models import Customer, HotelOwner


class UserApiViewTest(BaseApiTestCase):
    def test_login(self) -> None:
        user = User.objects.first()
        credentials = {
            'username': user.username,
            'password': TEST_PASSWORD
        }
        response = self.client.post(reverse('account:token_obtain_pair'), credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertIn('refresh', data.keys())
        self.assertIn('access', data.keys())
        self.assertIsInstance(data['refresh'], str)
        self.assertIsInstance(data['access'], str)

    def test_create_user_with_invalid_group_name(self) -> None:
        body = {
            'username': 'johnny',
            'first_name': 'johnny',
            'last_name': 'cash',
            'email': 'johnny@gmail.com',
            'password': 'Secret123',
            'group_name': "Unknown group",
            'country': 'POLAND',
            'date_of_birth': '1999-03-12'
        }
        response = self.client.post(reverse('account:create-list-view'), body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "This group doesn't exist! Only Hotel Owner, Customer is allowed!")

    def test_create_user(self) -> None:
        body = {
            'username': 'johnny',
            'first_name': 'johnny',
            'last_name': 'cash',
            'email': 'johnny@gmail.com',
            'password': 'Secret123',
            'group_name': G_CUSTOMER,
            'country': 'POLAND',
            'date_of_birth': '1999-03-12'
        }

        response = self.client.post(reverse('account:create-list-view'), body)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User was created!')
        user = User.objects.prefetch_related('profile', 'groups') \
            .filter(username=body['username']).first()
        self.assertIsNotNone(user)

        self.assertEqual(body['username'], user.username)
        self.assertEqual(body['first_name'], user.first_name)
        self.assertEqual(body['last_name'], user.last_name)
        self.assertEqual(body['email'], user.email)
        self.assertTrue(user.groups.filter(name=body['group_name']).exists())
        self.assertEqual(body['country'].lower(), user.profile.country)
        self.assertEqual(body['date_of_birth'], user.profile.date_of_birth.strftime('%Y-%m-%d'))

        response = self.client.post(reverse('account:create-list-view'), body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user(self) -> None:
        response = self.client.get(reverse('account:create-list-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), settings.REST_FRAMEWORK['PAGE_SIZE'])

    def _validate_user_data_from_response(self, data: dict, user: User) -> None:
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['country'], user.profile.country)
        self.assertEqual(data['date_of_birth'], f'{user.profile.date_of_birth:%Y-%m-%d}')

    def test_update_user(self) -> None:
        user = User.objects.first()
        pk = user.pk
        self.client.force_authenticate(user)
        body = {
            'date_of_birth': '2000-03-19',
            'country': 'France',
            'last_name': 'Cash',
            'first_name': 'Johnny'
        }

        response = self.client.put(reverse('account:retrieve-update-delete-view', kwargs={'pk': pk}), body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self._validate_user_data_from_response(response.data, user)

    def test_retrieve_user(self) -> None:
        user = User.objects.prefetch_related('profile', 'groups').first()
        self.client.force_authenticate(user)
        response = self.client.get(reverse('account:retrieve-update-delete-view', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user_data_from_response(response.data, user)
        self.assertEqual(response.data['groups'][0], f'{user.groups.all()[0].name}')

    def test_delete_user(self) -> None:
        amount_of_users = User.objects.count()
        user = User.objects.first()
        pk = user.id
        self.client.force_authenticate(user)
        response = self.client.delete(reverse('account:retrieve-update-delete-view', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), amount_of_users - 1)
        self.assertIsNone(User.objects.filter(pk=pk).first())


class CustomerAndHotelOwnerListApiView(BaseApiTestCase):
    def _base_test_case(self, view_name: str) -> list:
        response = self.client.get(reverse(view_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['results']

    def test_customers_view(self) -> None:
        results = self._base_test_case('account:customers')
        self.assertEqual(len(results), Customer.objects.count())

    def test_hotel_owners_view(self) -> None:
        results = self._base_test_case('account:hotel-owners')
        self.assertEqual(len(results), HotelOwner.objects.count())
