from rest_framework import serializers
from student.models import (
                             Pupil,
                             PupilClassesCoursesGrades,
                             PupilClassesAcknowledgments,
                             SpecialCoursesPerDesiredChoice
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

class PupilAcknowledgmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model= PupilClassesAcknowledgments
        fields= "__all__"
        read_only_fields = ['ack_points']

# Maybe we don't need it;
class PupilSpecialCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model= SpecialCoursesPerDesiredChoice
        field= "__all__"
