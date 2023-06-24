from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from user.models import User, Program


class Command(BaseCommand):
    help = 'Create users'

    def handle(self, *args, **options):

        for i in range(1,11):
            owner_email = f'web{i}@email.com'
            owner = User.objects.create(
                email=owner_email,
                first_name=f"web{i}",
                last_name=f'last{i}',
                is_active=True,
                phone_number='+919870661438',
                usn='1MV20IS027',
                program_selected=Program.objects.first(),
                proficiency=User.Proficiency.AVERAGE
            )
            owner.set_password("#Password008")
            owner.save()

        for i in range(1,11):
            owner_email = f'app{i}@email.com'
            owner = User.objects.create(
                email=owner_email,
                first_name=f"app{i}",
                last_name=f'last{i}',
                is_active=True,
                phone_number='+919870661438',
                usn='1MV20IS027',
                program_selected=Program.objects.last(),
                proficiency=User.Proficiency.AVERAGE
            )
            owner.set_password("#Password008")
            owner.save()

        self.stdout.write(self.style.SUCCESS('Data created successfully.'))
