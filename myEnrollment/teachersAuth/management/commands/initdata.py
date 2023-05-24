from django.core.management import BaseCommand, call_command
from teachersAuth.models import Teacher # from yourapp.models import User # if you have a custom user
from secondarySchools.fixtures import *

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        # app: secondarySchools fixtures
        call_command('loaddata','initdata-cantons')
        call_command('loaddata','initdata-secondary-schools')
        call_command('loaddata','initdata-courses')
        # app: teachersAuth fixtures
        call_command('loaddata','initdata-teacher')
        # Fix the passwords of fixtures
        for t in Teacher.objects.all():
            t.set_password(t.password)
            t.save()
        # app: student fixtures
        call_command('loaddata','initdata-class')
        call_command('loaddata','initdata-pupil')
        call_command('loaddata','initdata-primary-courses')
        call_command('loaddata','initdata-class-grades')
        # app: primarySchools fixtures
        # call_command('loaddata','initdata-primary-schools')

        # #initdata file is created combining multiple files from other fixtures
        # app_name = __package__.split('.')[0]
        # myFile= app_name+"/fixtures/initdata.json"
        # # open all files
        # with open('first.txt','r') as firstfile, open(myFile,'a') as destFile:
        #     # read content from first file
        #     for line in firstfile:
        #         # append content to second file
        #         destFile.write(line)
