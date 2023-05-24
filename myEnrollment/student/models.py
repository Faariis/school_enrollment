from django.db import models
from django.core.validators import RegexValidator

from secondarySchools.models import (
                                      SecondarySchool
                                    )
from primarySchools.models import (
                                    PrimarySchool
                                  )
####  ----------------- MODELS -----------------
class Acknowledgment(models.Model):
    ack_name= models.CharField(max_length=100)
    ack_points= models.IntegerField
    class Meta:
        db_table= 'Acknowledgments'

class SecondaryStudent(models.Model):
    # create model later for primary school, rename field to primary_school_id, fk
    primary_school= models.ForeignKey(PrimarySchool, on_delete= models.CASCADE,
                                      related_name='student_primary_school')
    secondary_shool_id= models.ForeignKey(SecondarySchool, on_delete= models.CASCADE,
                                       related_name= 'student_secondary_school')
    name= models. CharField(max_length=30)
    last_name= models. CharField(max_length=50)
    address= models.CharField(max_length=60)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must be entered in the format: '+<387xxxxxxx>'. Up to 12 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    null= True,
                                    blank=True) # Validators should be a list
    email= models.EmailField(null= True)
    year_of_enrollment= models.DateField(auto_now_add= True)
    spec_case_choices=(
                       ('regular','Regular student'),
                       ('invalid','Invaliditet'),
                       ('others','Ostali'),
                      )
    special_case= models.CharField(choices= spec_case_choices, default= 'regular')
    # Check how to fit this
    acknowledgment= models.ForeignKey(Acknowledgment, on_delete=models.CASCADE,
                                      related_name= 'student_acknowledgment')

    def __str__(self):
        return "%s" % (self._canton_code)
    class Meta:
        db_table= 'secondaryStudents'
