from django.db import models
from django.core.validators import RegexValidator

from secondarySchools.models import (
                                      SecondarySchool
                                    )
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
####  ----------------- MODELS -----------------
"""
  Acknowledgment model - specijalna priznanja
"""
class Acknowledgment(models.Model):
    ack_name= models.CharField(max_length=100)
    ack_points= models.PositiveIntegerField()
    class Meta:
        db_table= 'acknowledgments'



"""
  Pupil model
"""
class Pupil(models.Model):
    # create model later for primary school, rename field to primary_school_id, fk
    # primary_school= models.ForeignKey(PrimarySchool, on_delete= models.CASCADE,
    #                                   related_name='student_primary_school')
    primary_school= models.CharField(max_length=50)
    secondary_shool_id= models.ForeignKey(SecondarySchool, on_delete= models.CASCADE,
                                          related_name= 'student_secondary_school')
    name= models.CharField(max_length=30)
    middle_name= models.CharField(max_length=30, null= True, blank= True)
    last_name= models. CharField(max_length=50)
    gender= models.CharField(max_length=20)
    address= models.CharField(max_length=60)
    guardian_name= models.CharField(max_length= 30)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must be entered in the format: '+<387xxxxxxx>'. Up to 12 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    null= True,
                                    blank=True) # Validators should be a list
    guardian_number= models.CharField(validators=[phone_regex], max_length=17,
                                    null= True,
                                    blank=True) # Validators should be a list
    guardian_email= models.EmailField(null= True, blank= True)
    email= models.EmailField(null= True, blank= True)
    date_of_enrollment= models.DateField(auto_now_add= True)
    spec_case_choices=(
                       ('regular','Regular student'),
                       ('invalid','Invaliditet'),
                       ('others','Ostali'),
                      )
    special_case= models.CharField(choices= spec_case_choices,
                                   default= 'regular',
                                   max_length=10)
    # Check how to fit this
    acknowledgment= models.ForeignKey(Acknowledgment, on_delete=models.CASCADE,
                                      related_name= 'student_acknowledgment',
                                      null= True,
                                      blank= True)

    def __str__(self):
        return "Student ID %s: %s %s" %(self.id, self.name, self.last_name)
    class Meta:
        db_table= 'pupils'
        constraints = [
            models.UniqueConstraint(fields=['name','last_name','address'],
                                    name='composite-pk-name-last_name-address')
        ]
@receiver(pre_save, sender=Pupil)
def pre_save_for_year_of_enrollment_fixture(sender, instance, **kwargs):
    if kwargs['raw']:
        instance.date_of_enrollment = timezone.now()


"""
  Classes
"""
class Class(models.Model):
    class_codes=(
                    ('I','1'),
                    ('II','2'),
                    ('III','3'),
                    ('IV','4'),
                    ('V','5'),
                    ('VI','6'),
                    ('VII','7'),
                    ('VIII','8'),
                    ('IX','9')
                    )
    _classes=models.CharField(choices= class_codes,
                              max_length= 5,
                              primary_key= True)
    class Meta:
        db_table= 'studentClass'
    def __str__(self):
        return "Razred %s" %(self._classes)


"""
  All Courses in Primary school
"""
class Courses(models.Model):
    # Think about to add choices of all possible combinations
    course_code= models.CharField(max_length=5,
                                  primary_key= True,
                                  unique= True)
    course_name= models.CharField(max_length=30,
                                  blank= True,
                                  null= True)

    def __str__(self):
        return "Predmet %s" %(self.course_code)
"""
  Pupil classes
  We can calculate total grade per class no need to store value
"""
class PupilClassesCoursesGrades(models.Model):
    pupil_id= models.ForeignKey(Pupil,
                                on_delete= models.CASCADE,
                                related_name='pupil_id')
    class_id= models.ForeignKey(Class,
                                on_delete= models.CASCADE,
                                related_name='pupil_class_id')
    course_code= models.ForeignKey(Courses,
                                   on_delete= models.CASCADE,
                                   related_name='pupil_courses_code')
    score= models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)],
                                       null= True,
                                       blank= True)

    behavior_grades=(
        ('5','odlican'),
        ('4','vrlo dobar'),
        ('3','dobar'),
        ('2','zadovoljava')
    )
    pupil_behavior= models.CharField(choices= behavior_grades,
                                     max_length= 10)
    class Meta:
        db_table= 'PupilClassesCoursesGrades'
        constraints = [
            models.UniqueConstraint(fields=['pupil_id','class_id','course_code'],
                                    name='composite-pk-pupil_id-class_id-course_code')
        ]