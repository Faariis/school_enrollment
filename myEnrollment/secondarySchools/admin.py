from django.contrib import admin
from secondarySchools.models import SecondarySchool, Canton, CoursesSecondarySchool

# Register your models here.
admin.site.register(Canton)
admin.site.register(SecondarySchool)
admin.site.register(CoursesSecondarySchool)
