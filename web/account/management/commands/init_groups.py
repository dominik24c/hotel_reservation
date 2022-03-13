from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from ...groups import GROUPS


class Command(BaseCommand):
    help = 'Initialize base groups.'

    def handle(self, *args, **options) -> None:
        count_saved_instances = 0
        for group_name in GROUPS:
            try:
                Group.objects.create(name=group_name)
                count_saved_instances += 1
            except IntegrityError:
                self.stderr.write(
                    f'This group already exists! '
                    f'{Group.__name__}.objects.create(name="{group_name}")')
        if count_saved_instances == 0:
            self.stdout.write('None of the groups have been created')
        else:
            self.stdout.write('Groups was saved!')
