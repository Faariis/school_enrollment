


from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import Teacher, Canton

class TeacherLoginSerializer(serializers.ModelSerializer):
    #canton_code = serializers.CharField(source='Canton._canton_code')
    #canton_code = serializers.PrimaryKeyRelatedField(many=True, read_only= True)
    canton_code= serializers.RelatedField(many=True, read_only= True)
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model= Teacher() # get_user_model()
        fields=('id', 'is_superuser', 'first_name', 'last_name','canton_code')
    # def create(self, validated_data):
    #     user = Teacher.objects.create_user(validated_data['email'], validated_data["password"])
    #     return user
    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['canton_name'] = TeacherLoginSerializer(instance.canton_name).data
    #     return rep
