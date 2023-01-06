


from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import Teacher

class TeacherLoginSerializer(serializers.ModelSerializer):
    canton_code = serializers.CharField(source='Canton._canton_code')
    class Meta:
        model= Teacher() # get_user_model()
        fields=('id', 'is_superuser', 'first_name', 'last_name')
    def create(self, validated_data):
        user = Teacher.objects.create_user(validated_data['email'], validated_data["password"])
        return user
