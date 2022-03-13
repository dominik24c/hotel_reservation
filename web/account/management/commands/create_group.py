from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create new group.'

    def add_arguments(self, parser) -> None:
        parser.add_argument('group_name', type=str)

    def handle(self, *args, **options) -> None:
        group_name = options['group_name']
        group = Group.objects.filter(name=group_name).first()

        if group is not None:
            raise CommandError('This group already exists!')
        else:
            Group.objects.create(name=group_name)
