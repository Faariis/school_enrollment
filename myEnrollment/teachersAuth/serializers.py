from rest_framework import serializers
from .models import Teacher
import django.contrib.auth

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'password']
        # Hide password return (for each field)
        extra_kwargs={
            'password':{'write_only':True}
        }

# Override default create method that is between view and model creation
def create(self, validated_data):
    # extract pass
    print("**Validated data before: ", **validated_data)
    my_password= validated_data.pop('password', None)
    print("Validated data after: ", validated_data)
    print("**Validated data after: ", **validated_data)
    # create teacher and pass data without password
    teacher= self.Meta.model(**validated_data)
   
    if my_password:
        # set_password() provided by Django and hashed
        teacher.set_password(my_password)
        print("U funckiji je moj pass: ", my_password)
    teacher.save()
    return teacher
