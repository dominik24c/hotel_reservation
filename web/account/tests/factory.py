import random
from datetime import datetime

import factory
from django.contrib.auth.models import User, Group
from factory import fuzzy
from factory.django import DjangoModelFactory

from ..groups import GROUPS
from ..models import Profile

TEST_PASSWORD = 'Secret123!'


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}user')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: f'test{n}user@mail.com')
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    country = factory.Faker("country")
    date_of_birth = factory.LazyFunction(datetime.now)


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = fuzzy.FuzzyChoice(GROUPS)


def create_groups() -> list[Group]:
    return [GroupFactory.create(name=group_name) for group_name in GROUPS]


def create_users_and_profiles(amount: int, groups: list[Group]) -> None:
    users = UserFactory.create_batch(amount)
    profiles = []
    for user in users:
        profiles.append(ProfileFactory.build(user=user))
        group_name = random.choices(groups)[0]
        user.groups.add(group_name)
    Profile.objects.bulk_create(profiles)
