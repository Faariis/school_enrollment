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
from rest_framework.generics import  ListCreateAPIView, ListAPIView
from rest_framework import status, mixins
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
                          TeacherSerializer,
                          SecondarySchoolSerializer,
                        )
from .models import (
                      Teacher,
                      SecondarySchool,
                      CoursesSecondarySchool
                    )
import myEnrollment.settings as api_settings

class ApiOverview(APIView):
    def get(self, request):
        api_urls = {
            'Get JWT token': '/api/login/',
            'Logout teacher': '/api/logout/',
            'Refresh JWT token': '/api/login/refresh/',
            'Get token and teacher info': '/api/teacher-token/',
            'List of all schools(admin), single school(non-admin)': '/api/shool-list',
            'List of all schools(admin), single school(non-admin)': '/api/shool-list/<int:pk>/',
        }
        return Response(api_urls)

#
# view for listing a queryset. ListAPIView
# view for retrieving a single model instance. RetrieveAPIView
# retrieving, updating a model instance. RetrieveUpdateAPIView
# listing a queryset or creating a model instance. ListCreateAPIView
# retrieving, updating or deleting a model instance. RetrieveUpdateDestroyAPIView

class TeacherView(ListCreateAPIView):
    queryset = Teacher.objects.all() # we use custom manager
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        teacher= Teacher.objects.get(id= request.auth['user_id'])

        # Only super user can see list of all schools and all users/extract only schools
        schools= Teacher.objects.values_list('school_id', flat=True).filter(id=teacher.id)
        if  teacher.is_superuser:
            # queryset = self.get_queryset()
            # serializer = TeacherSerializer(queryset, many=True)
            serializer= SecondarySchoolSerializer(schools, many= True)
            return Response(serializer.data)
        else:
            # Teacher can belong to single school only and see only course to edit for that school
            # TODO: teacher can edit only courses he belongs to
            
            non_admin_schools= schools[0] # from QS to string
            school_id_queryset= SecondarySchool.objects.get(id= non_admin_schools)
            school_id= school_id_queryset[0]
            course_school_id= CoursesSecondarySchool.objects.get(school_id= school_id)
            serializer = SecondarySchoolSerializer(school_id_queryset)
            return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response
