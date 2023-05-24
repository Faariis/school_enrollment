from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django_countries.fields import CountryField

####  ----------------- MODELS -----------------
class Canton(models.Model):
    _canton_code= models.CharField(max_length=3, default='ZDK', primary_key=True)
    canton_name= models.CharField(max_length=50, default='Zenicko-dobojski')
    country= CountryField(default='BA')
    def __str__(self):
        return "%s" % (self._canton_code)
    class Meta:
        db_table= 'cantons'


# """
#   Nastavni planovi i programi po kantonu
# """
# class CantonNPPPrimarySchool(models.Model):
#     npp_choices=(
#         ('BOS','BOS'),
#         ('HRV','HRV'),
#         ('SRP','SRP')
#     )
#     npp_code= models.CharField(max_length=3,
#                                default='BOS',
#                                choices= npp_choices,
#                                unique= True)
#     npp_canton= models.ForeignKey(Canton, default='ZDK',
#                                   on_delete=models.CASCADE,
#                                   related_name='npp_canton')
#     def __str__(self):
#         return "%s" % (self._canton_code)
#     class Meta:
#         db_table= 'cantonsNPPPrimary'
#         constraints = [
#             models.UniqueConstraint(fields=['npp_code','npp_canton'],
#                                     name='composite-pk-npp_code-npp_canton')
#         ]
#     @classmethod
#     def get_default_pk(cls):
#         obj, created = cls.objects.get_or_create(
#             npp_code='BOS',
#             npp_canton= 'ZDK',
#             defaults={'npp_code':'BOS', 'npp_canton':'ZDK'}
#         )
#         return obj.pk


class SecondarySchool(models.Model):
    school_name= models.CharField(max_length=100, default='Tehnicka skola Zenica', unique=True)
    school_address= models.CharField(max_length=100, default='Bilimisce 28, Zenica')
    school_email= models.EmailField(null= True, blank= True)
    # Many schools can belong to one canton
    school_canton_code= models.ForeignKey(Canton, default='ZDK',
                                          on_delete=models.CASCADE,
                                          related_name='school_canton')
    def __str__(self):
        return "%s - %s" % (self.school_name, self.school_canton_code)
    class Meta:
        db_table= 'secondarySchools'

class CoursesSecondarySchool(models.Model):
    three_year='III'
    four_year='IV'
    duration_choices=[
                      (three_year, 'Trogodisnje'),
                      (four_year, 'Cetverogodisnje')
                     ]
    _course_code= models.CharField(primary_key=True, max_length=20)
    course_name= models.CharField(max_length=100)
    course_duration= models.CharField(max_length=10, choices= duration_choices, default=four_year)
    school_id= models.ForeignKey(SecondarySchool, on_delete=models.CASCADE,
                                 related_name='courses_secondary')
    def __str__(self):
        return self._course_code
    class Meta:
        db_table='courses_secondary'
        constraints = [
            models.UniqueConstraint(fields=['school_id','_course_code'],
                                    name='composite-pk-school_id-course_code')
        ]


# Since USERNAME is email is unique I cannot add multiple records of email/courses
# but can do authentication https://stackoverflow.com/questions/31370118/multiple-username-field-in-django-user-model

# class Grade(models.Model):
#     # ocjena moze biti null - vjeronauka
#     ocjena= models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)], null=True)
#     # we want to know which teacher inserted the grade
#     nastavnik= models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="grades")
#     def __str__(self):
#         return "%s - %s", str(self.ocjena), self.nastavnik.email_user
