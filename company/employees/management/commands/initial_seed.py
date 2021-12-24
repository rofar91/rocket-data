import random

from django.core import management
from django.core.management.base import BaseCommand
from django_seed import Seed
from rest_framework.authtoken.models import Token

from employees.models import SalaryHistory, Employee


class Command(BaseCommand):
    help = 'Initial seed DB'

    def handle(self, *args, **options):
        # seed ranks, employees, groups from fixtures
        management.call_command('loaddata', 'ranks', verbosity=0)
        management.call_command('loaddata', 'groups_permission', verbosity=0)
        management.call_command('loaddata', 'employees', verbosity=0)

        # seed salary history used django-seed
        seeder = Seed.seeder()
        seeder.add_entity(SalaryHistory, 10, {
            'employee': lambda x: Employee.objects.get(id=random.randint(1, 5)),
            'amount_of_payment': lambda x: random.randint(1, 1234567890)/100,
        })
        seeder.execute()

        # create token
        Token.objects.get_or_create(user_id=1)

        self.stdout.write(self.style.SUCCESS('Successfully seed DB'))
