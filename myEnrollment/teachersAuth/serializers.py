


from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import (
                      Teacher,
                      Canton,
                      SecondarySchool,
                      CoursesSecondarySchool
                    )

# Model serializer .create.update is automatically created compared to serializers.Serializer
# There also exist serializers.HyperlinkedModelSerializer where instead of ID url is generated

class CantonSerializer(serializers.ModelSerializer):
    class Meta:
        model= Canton
        fields= "__all__"

class CoursesSecondarySchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= CoursesSecondarySchool
        fields= "__all__"

# Nested relations of serialiser https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
class SecondarySchoolSerializer(serializers.ModelSerializer):
    # To get many teacher from this school. Variable name MUST be same as related_name
    # read_only means that we cannot add cantons through post request
    school_canton= CantonSerializer(many=True, read_only= True) # this will return all data about teacher
    # To control what to show: __str__
    # school_id= serializers.StringRelatedField(many=True) # this will return teacher.__str__
    # school_id= serializers.PrimaryKeyRelatedField(many=True, ready_only=True) # returns only primary keys
    # school_id= serializers.HyperlinkedRelatedField(many=True, ready_only=True, view_name="secondarySchools-detail") # view name: <model>-detail
    # For above when using in get method qs=objects.all(), SecondarySchoolSerializer(qs, many=True, context={'request':request})
    # What if there are multiple foreignkeys?
    # school_id= serializers.HyperlinkedIdentityField(view_name='track-list') # used as link identity to id
    class Meta:
        model= SecondarySchool
        fields= "__all__"
        depth= 2


class TeacherSerializer(serializers.ModelSerializer):
    #canton_code = serializers.CharField(source='Canton._canton_code')
    #canton_code = serializers.PrimaryKeyRelatedField(many=True, read_only= True)
    # canton_code= serializers.RelatedField(many=True, read_only= True)
    # Exclude many=True for not-iterable objects
    school_id= SecondarySchoolSerializer(read_only= True)
    course_code= CoursesSecondarySchoolSerializer(read_only= True)
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # Create custom serializer field with get_<name-field> method
    # It will be part of response, it can be used for example of login duration


    class Meta:
        model= Teacher() # get_user_model()
        # fields="__all__"
        exclude = ['password', 'groups']
    
    # === Methods ====
    # def get_is_super_user(self, object):
    #     return object.is_superuser
    
    # For serializer.Serializer validation: https://www.django-rest-framework.org/api-guide/serializers/#validation
    # Validation is done the same
    # This is object validator for all object when is_valid() is called
    def validate(self, data):
        if data['first_name'] == data['last_name']:
            raise serializers.ValidationError("Last name and first name cannot be the same")
        return data
    
    # This is field validator validate_<field_name> / one can use validators for serializer.Serializer
    def validate_first_name(self, value):
        if value < 3:
            raise serializers.ValidationError("Last name cannot be less than 3")
        return value

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['canton_name'] = TeacherLoginSerializer(instance.canton_name).data
    #     return rep

    # This is not needed, for model serializer
    # def create(self, validated_data):
    #     user = Teacher.objects.create_user(validated_data['email'], validated_data["password"])
    #     return user