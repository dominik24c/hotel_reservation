from rest_framework.test import APITestCase


class BaseApiTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        from account.tests.factory import create_users_and_profiles, create_groups
        create_users_and_profiles(10, create_groups())

    def setUp(self) -> None:
        from django.contrib.auth.models import User
        user = User.objects.first()
        self.client.force_authenticate(user)
