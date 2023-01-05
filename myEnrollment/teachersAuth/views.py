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
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

from .serializers import TeacherLoginSerializer
from .models import Teacher, update_last_and_previous_login
import jwt, datetime
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

class TeacherLoginView(RetrieveAPIView): #RetrieveAPIView)
    permission_classes = (IsAuthenticated,)
    # lookup_field = "pk"
    # queryset=Teacher.objects.all()
    serializer_class = TeacherLoginSerializer
    #import pdb
    #pdb.set_trace()
    # def get_queryset(self):
    #     return Teacher.objects.all()

    # def get(self, request, *args, **kwargs):
    #     serializer= self.serializer(data=request.user)
    #     serializer.is_valid(raise_exception= True)
    #     status_code = status.HTTP_200_OK
    #     response={
    #         'success':'True',
    #         'status_code': status_code,
    #         'message': 'Teacher logged in  successfully',
    #         'token' : serializer.data['jwt_token'],
    #     }
    #     return Response(response, status= status_code)

    def get_object(self):
        print(self.request.user)
        return self.request.user
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # make sure to catch 404's below
    #     obj = queryset.get(id=self.request.user.id)
    #     self.check_object_permissions(self.request, obj)
    #     return obj

class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response
