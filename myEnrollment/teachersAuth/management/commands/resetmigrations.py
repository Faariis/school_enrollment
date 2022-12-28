from django.core.management.base import BaseCommand, CommandError
import os

class Command(BaseCommand):
    help= 'MyManagment:TeachersAuth: reset/remove migration'
    def handle(self, *args, **options):
        app_name = __package__.split('.')[0]
        command= "find " +app_name + "/migrations "+ "-name '*.py' -not -name '__init__.py' -delete"
        res= os.system(command)
        if res:
          raise CommandError("Migration files not found")
        else:
          self.stdout.write(self.style.SUCCESS('Migration files deleted'))

        # Clear cache
        command= "find " +app_name + "/migrations "+ "-name '*.pyc' -delete"
        res= os.system(command)
        if res:
            raise CommandError("Migration files not found")
        else:
            self.stdout.write(self.style.SUCCESS('Migration cache deleted'))