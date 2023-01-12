


from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from teachersAuth.models import  Teacher

from secondarySchools.serializers import  (
                                            SecondarySchoolSerializer,
                                            CoursesSecondarySchoolSerializer
                                          )
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

# Model serializer .create.update is automatically created compared to serializers.Serializer
# There also exist serializers.HyperlinkedModelSerializer where instead of ID url is generated

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Teacher
        fields = ['token']


class TeacherSerializerList(serializers.ModelSerializer):
    #school_id= SecondarySchoolSerializer(many=True, read_only=True)
    #course_code= CoursesSecondarySchoolSerializer(many=True, read_only= True)

    class Meta:
        model= Teacher
        fields= ['email', 'password', 'first_name', 'last_name',
                'is_staff', 'school_id', 'course_code']
        depth= 2

# used to hide hashed password
class TeacherSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model= Teacher
        exclude = ['password', 'groups', 'user_permissions', 'date_joined',
                   'previous_login', 'last_login', 'is_active']
    
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


class LoginSerializer(serializers.ModelSerializer):
    email= serializers.EmailField(max_length=255, min_length= 3)
    password= serializers.CharField(write_only= True) # don't return to user
    # tokens= models.CharField(max_length=555, read_only= True) # don't ask user about, just return it to user
    tokens= serializers.SerializerMethodField()

    class Meta:
        model= Teacher
        fields= ['email', 'password', 'tokens']

    def get_tokens(self, obj):
        user = Teacher.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    
    def validate(self, obj):
        email= obj['email']
        password_raw= obj['password']
        filtered_user_by_email = Teacher.objects.filter(email=email)
        if filtered_user_by_email:
            password= filtered_user_by_email[0].set_password(password_raw)
        else:
             raise AuthenticationFailed('No such user with email')
        import pdb; pdb.set_trace()
        user = auth.authenticate(email=email, password=password)
        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'tokens': user.tokens
        }
