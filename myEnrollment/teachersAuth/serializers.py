


from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from teachersAuth.models import  Teacher

from secondarySchools.serializers import  (
                                            SecondarySchoolSerializer,
                                            CoursesSecondarySchoolSerializer
                                          )
# Model serializer .create.update is automatically created compared to serializers.Serializer
# There also exist serializers.HyperlinkedModelSerializer where instead of ID url is generated


class TeacherSerializer(serializers.ModelSerializer):
    #canton_code = serializers.CharField(source='Canton._canton_code')
    #canton_code = serializers.PrimaryKeyRelatedField(many=True, read_only= True)
    # canton_code= serializers.RelatedField(many=True, read_only= True)
    # Exclude many=True for not-iterable objects
    # school_id= SecondarySchoolSerializer(read_only= True)
    # course_code= CoursesSecondarySchoolSerializer(read_only= True)
    # course_code= CoursesSecondarySchoolSerializer
    # school_id= SecondarySchoolSerializer
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # Create custom serializer field with get_<name-field> method
    # It will be part of response, it can be used for example of login duration


    class Meta:
        model= Teacher # get_user_model()
        # fields="__all__"
        # fields= ['email', 'password', 'first_name', 'last_name'
        #          'is_staff', 'school_id', 'course_code']
        exclude = ['groups', 'user_permissions', 'date_joined',
                   'previous_login', 'last_login', 'is_active']
    
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
        if value is None or value == '':
            raise serializers.ValidationError("First name cannot be empty")
        if len(value) < 3:
            raise serializers.ValidationError("Last name cannot be less than 3")
        return value
    def valida_last_name(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("Last name cannot be empty")
    def validate_school_id(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("School ID has to be integer")
    def validate_course_code(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("Course ID has to be string")
    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['canton_name'] = TeacherLoginSerializer(instance.canton_name).data
    #     return rep

    # This is not needed, for model serializer
    # def create(self, validated_data):
    #     user = Teacher.objects.create_user(validated_data['email'], validated_data["password"])
    #     return user
