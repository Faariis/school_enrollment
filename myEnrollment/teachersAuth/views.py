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
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import  (
                                      ListCreateAPIView,
                                      ListAPIView,
                                      CreateAPIView,
                                      RetrieveUpdateDestroyAPIView
                                     )
from rest_framework import status, mixins
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
                          CantonSerializer,
                          TeacherSerializer,
                          SecondarySchoolSerializer,
                          CoursesSecondarySchoolSerializer
                        )
from .models import (
                      Teacher,
                      Canton,
                      SecondarySchool,
                      CoursesSecondarySchool
                    )
import myEnrollment.settings as api_settings

# view for listing a queryset. ListAPIView
# view for retrieving a single model instance. RetrieveAPIView
# retrieving, updating a model instance. RetrieveUpdateAPIView
# listing a queryset or creating a model instance. ListCreateAPIView
# retrieving, updating or deleting a model instance. RetrieveUpdateDestroyAPIView

class ApiOverview(APIView):
    def get(self, request):
        api_urls = {
            'API overview': '/api/',
            'Get JWT token': '/api/login/',
            'Logout teacher': '/api/logout/',
            'Refresh JWT token': '/api/login/refresh/',
            
            'List all cantons': '/api/canton/',
            'GET/UPDATE/DELETE cantons by canton code(like zdk)': '/api/canton/<canton_code>/',

            'GET all schools from canton or CREATE a scohol in a canton':'/api/canton/schools/<canton_code>/',
            'GET/POST/PUT/DELETE school from list by pk':'/api/canton/schools/<pk>',

            'List of all schools and create new school visible by logged teacher': '/api/school-list/',
            'GET/POST/PUT/DELETE school by id': '/api/school-list/<int:pk>/',
            'CREATE course for school by id': '/api/school-list/<int:pk>/course-create/',
            'GET all course school by id': '/api/school-list/<int:pk>/courses/',

         }
        return Response(api_urls)


class SchoolView(ListCreateAPIView):
    # queryset = SecondarySchool.objects.all() # we use custom manager
    serializer_class = SecondarySchoolSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SecondarySchool.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        teacher= Teacher.objects.get(id= request.auth['user_id'])
        # teacher= Teacher.objects.get(id= 1)
        schools= Teacher.objects.values_list('school_id', flat=True).filter(id=teacher.id)
        school_id_queryset= SecondarySchool.objects.get(id= schools[0])
        serializer= SecondarySchoolSerializer(school_id_queryset)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        # Only superuser can create new school
        is_superuser= Teacher.objects.get(id= request.auth['user_id']).is_superuser
        # is_superuser=1 
        if is_superuser:
            serializer= SecondarySchoolSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status.HTTP_403_FORBIDDEN)

class SchoolViewDetail(RetrieveUpdateDestroyAPIView):
    queryset= SecondarySchool.objects.all()
    serializer_class= SecondarySchoolSerializer
    # Only superuser can update school
    permission_classes= [IsAdminUser]

# On single object
class SchoolCoursesCreateView(CreateAPIView):
    serializer_class= CoursesSecondarySchoolSerializer
    permission_classes= [IsAdminUser]
    def perform_create(self, serializer):
        pk= self.kwargs['pk']
        school= SecondarySchool.objects.get(id= pk)
        serializer.save(school_id= school)

class SchoolCoursesListView(ListAPIView):
    serializer_class= CoursesSecondarySchoolSerializer
    permission_classes= [IsAdminUser]
    def get_queryset(self):
        pk= self.kwargs['pk']
        return CoursesSecondarySchool.objects.filter(school_id=pk)

class CantonView(ListAPIView):
    permission_classes= [IsAdminUser]
    queryset= Canton.objects.all()
    serializer_class= CantonSerializer

class CantonDetailView(RetrieveUpdateDestroyAPIView):
    queryset= Canton.objects.all()
    lookup_field="canton_code"
    serializer_class= SecondarySchoolSerializer
    permission_classes= [IsAdminUser]

class CantonSchoolView(ListCreateAPIView):
    serializer_class= SecondarySchoolSerializer
    permission_classes= [IsAdminUser]

    def get_queryset(self):
        school_canton_code= self.kwargs['canton_code']
        obj= SecondarySchool.objects.filter(school_canton_code=school_canton_code)
        return obj

    def list(self, request, *args, **kwargs):
        queryset= self.get_queryset()
        serializer= SecondarySchoolSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        school_canton_code= self.kwargs['canton_code']
        school_canton_code_obj= Canton(_canton_code= school_canton_code)
        serializer= SecondarySchoolSerializer(data=request.data)
        if  serializer.is_valid():
            serializer.save(school_canton_code= school_canton_code_obj)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class CantonSchoolDetailView(RetrieveUpdateDestroyAPIView):
    queryset= SecondarySchool.objects.all()
    serializer_class= SecondarySchoolSerializer
    permission_classes= [IsAdminUser]
    

class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response
