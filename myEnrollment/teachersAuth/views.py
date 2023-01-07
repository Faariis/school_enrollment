import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from django.utils.translation import gettext_lazy as g4
django.utils.translation.ugettext_lazy= g4
django.utils.translation.ugettext= g4

#from django.utils.translation import ugettext, ugettext_lazy as _
# https://stackoverflow.com/questions/71420362/django4-0-importerror-cannot-import-name-ugettext-lazy-from-django-utils-tra
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, GenericAPIView
from rest_framework import status, mixins

from .serializers import TeacherLoginSerializer, SecondarySchoolSerializer, CantonSerializer 
from .models import Teacher, SecondarySchool, Canton
import myEnrollment.settings as api_settings

class ApiOverview(APIView):
    def get(self, request):
        api_urls = {
            'all teachers': '/',
            'Search by teachers first_name': '/?first_name=first_name',
            'Search by teachers last_name': '/?last_name=last_name',
            'Search by teachers canton': '/?canton=canton',
            'Add teacher': '/teacher/register',
            'Update teacher': '/teacher/update/pk',
            'Delete teacher': '/teacher/delete/pk'
        }
        return Response(api_urls)

#
# view for listing a queryset. ListAPIView
# view for retrieving a model instance. RetrieveAPIView
# retrieving, updating a model instance. RetrieveUpdateAPIView
# listing a queryset or creating a model instance. ListCreateAPIView
# retrieving, updating or deleting a model instance. RetrieveUpdateDestroyAPIView

class TeacherLoginView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    queryset=Teacher.objects.all()
    serializer_class = TeacherLoginSerializer

    def get_object(self):
        return self.request.user

class TeachersList(ListCreateAPIView):
    queryset = Teacher.ab_ob.all() # we use custom manager
    serializer_class = TeacherLoginSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = TeacherLoginSerializer(queryset, many=True)
        return Response(serializer.data)

class TeachersList2(mixins.ListModelMixin, GenericAPIView):
    queryset= Teacher.objects.all()
    serializer_class=TeacherLoginSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response
