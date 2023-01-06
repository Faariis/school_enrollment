


from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import Teacher

class TeacherLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model= Teacher() # get_user_model()
        fields=('id', 'is_superuser', 'first_name', 'last_name')
