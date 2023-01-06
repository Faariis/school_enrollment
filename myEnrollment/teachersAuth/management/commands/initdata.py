from django.core.management import BaseCommand, call_command
from  teachersAuth.models import Teacher # from yourapp.models import User # if you have a custom user


class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata','initdata')
        # Fix the passwords of fixtures
        for t in Teacher.objects.all():
            t.set_password(t.password)
            t.save()
