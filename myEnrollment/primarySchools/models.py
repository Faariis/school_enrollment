from django.db import models
from secondarySchools.models import (
                                      CantonNPP
                                    )
####  ----------------- MODELS -----------------
"""
  Razredi: 1-9
"""
class PrimarySchoolClass(models.Model):
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
    _school_class_code=models.CharField(choices=class_codes)
    class Meta:
        db_table= 'primarySchoolClasses'


"""
  Predmeti u osnovnoj skoli
"""
class PrimarySchoolCourses(models.Model):
    _course_code=models.CharField(max_length=50, primary_key= True)
    class Meta:
        db_table= 'primarySchoolCourses'



"""
  Predmeti u osnovnoj skoli po kantonu
"""
class CoursesPrimarySchoolCantonNPP(models.Model):
    course_class= models.ForeignKey(PrimarySchoolClass, on_delete= models.CASCADE,
                                    related_name='course_primary_school_class')
    course_name= models.ForeignKey(PrimarySchoolCourses, on_delete= models.CASCADE,
                                   related_name='course_primary_school_name')
    course_canton_npp= models.ForeignKey(CantonNPP, default='BOS',
                                         on_delete=models.CASCADE,
                                         related_name='course_primary_school_canton')
    def __str__(self):
        return "Primary: %s - %s" % (self.school_name, self.school_canton_code)
    class Meta:
        db_table= 'CantonPrimarySchoolCourses'


"""
  Osnovna skola- preko kantona dodjem do predmeta
"""
class PrimarySchool(models.Model):
    school_name= models.CharField(max_length=100, default='Edhem Mulabdić Zenica', unique=True)
    school_address= models.CharField(max_length=100, default='Bilimisce 63, Zenica')
    # Many schools can belong to one canton
    school_canton_code= models.ForeignKey(Canton, default='ZDK',
                                          on_delete=models.CASCADE,
                                          related_name='primary_school_canton')
    def __str__(self):
        return "Primary: %s - %s" % (self.school_name, self.school_canton_code)
    class Meta:
        db_table= 'primarySchools'
