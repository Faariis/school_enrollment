from rest_framework import serializers
from secondarySchools.models import (
                                      Canton,
                                      CoursesSecondarySchool,
                                      SecondarySchool
                                    )

class CantonSerializer(serializers.ModelSerializer):
    class Meta:
        model= Canton
        # To include reverse relation of child tables explicitly add in list
        fields= ['_canton_code', 'canton_name', 'country', 'school_canton']
        # fields="__all__"

class CoursesSecondarySchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= CoursesSecondarySchool
        # fields= "__all__"
        exclude=('school_id',)


# Nested relations of serialiser https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
class SecondarySchoolSerializer(serializers.ModelSerializer):
    # To get many teacher from this school. Variable name MUST be same as related_name
    # read_only means that we cannot add cantons through post request
    # school_canton= CantonSerializer(read_only= True) # this will return all data about teacher
    # To control what to show: __str__
    # school_id= serializers.StringRelatedField(many=True) # this will return teacher.__str__
    # school_id= serializers.PrimaryKeyRelatedField(many=True, ready_only=True) # returns only primary keys
    # school_id= serializers.HyperlinkedRelatedField(many=True, ready_only=True, view_name="secondarySchools-detail") # view name: <model>-detail
    # For above when using in get method qs=objects.all(), SecondarySchoolSerializer(qs, many=True, context={'request':request})
    # What if there are multiple foreignkeys?
    # school_id= serializers.HyperlinkedIdentityField(view_name='track-list') # used as link identity to id
    class Meta:
        model= SecondarySchool
        # fields= "__all__"
        # depth= 1
        fields= ['id', 'school_name', 'school_address', 'school_canton_code',
                 'courses_secondary']

