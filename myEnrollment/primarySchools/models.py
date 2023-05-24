from django.db import models
from secondarySchools.models import (
                                      Canton
                                    )
from django.core.validators import MinValueValidator,MaxValueValidator

"""
  Osnovna skola- preko kantona dodjem do predmeta
"""
# class PrimarySchool(models.Model):
#     school_name= models.CharField(max_length=100, default='Edhem Mulabdić Zenica', unique=True)
#     school_address= models.CharField(max_length=100, default='Bilimisce 63, Zenica')
#     email= models.EmailField(null= True)
#     # Many schools can belong to one canton
#     school_canton_code_npp= models.ForeignKey(Canton,
#                                               on_delete=models.CASCADE,
#                                               related_name='primary_school_canton')
#     def __str__(self):
#         return "Primary: %s - %s" % (self.school_name, self.school_canton_code)
#     class Meta:
#         db_table= 'primarySchools'