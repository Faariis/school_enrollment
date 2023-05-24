from rest_framework import serializers
from student.models import (
                             Pupil,
                             PupilClassesCoursesGrades
                           )

class PupilSerializer(serializers.ModelSerializer):
    class Meta:
        model= Pupil
        # To include reverse relation of child tables explicitly add in list
        # fields= ['_canton_code', 'canton_name', 'country', 'school_canton']
        fields="__all__"

class PupilCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model= PupilClassesCoursesGrades
        fields= "__all__"
