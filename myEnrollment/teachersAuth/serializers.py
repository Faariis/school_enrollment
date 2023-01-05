


from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import Teacher
import django.contrib.auth

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class TeacherLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except Teacher.DoesNotExist:
            raise serializers.ValidationError(
                'Teacher with given email and password does not exists'
            )
        return {
            'email':user.email,
            'jwt_token': jwt_token
        }
    
'''
# Not used

class TeacherCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        # Hide password return (for each field)
        extra_kwargs={
            'password':{'write_only':True}
        }

    # Override default create method that is between view and model creation
    def create(self, validated_data):
        # extract pass
        my_password= validated_data.pop('password', None)
        print("Validated data after: ", validated_data)
        # create teacher and pass data without password
        instance= self.Meta.model(**validated_data)
        print("MyCountry",instance.country)
        if my_password:
            # set_password() provided by Django and hashed
            instance.set_password(my_password)
            print("U funckiji je moj pass: ", my_password)

        instance.save()
        return instance

'''