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
from rest_framework  import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from teachersAuth.serializers import TeacherSerializer
from teachersAuth.models import Teacher

from secondarySchools.models import SecondarySchool,CoursesSecondarySchool
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

            'Admin can create new teacher':'/api/teacher-create/',
            
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

class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response

class TeacherCreateView(CreateAPIView):
    serializer_class= TeacherSerializer
    permission_classes= [IsAdminUser]
    # queryset= Teacher.ab_ob.all()

    def post(self, request):
        # We have to check school and course_code  
        school_id= request.data['school_id']
        course_code= request.data['school_id']

        school= SecondarySchool.objects.filter(school_id= school_id).first()
        if school is None:
            return Response({"error": "wrong school"}, status=status.HTTP_400_BAD_REQUEST)
        school_course= CoursesSecondarySchool.objects.filter(course_code= course_code).first()
        if school_course is None:
            return Response({"error": "wrong school"}, status=status.HTTP_400_BAD_REQUEST)

        serializer= TeacherSerializer(data= request.data)

        if serializer.is_valid():
            # self.pre_save(serializer.object)
            # self.object = serializer.save(force_insert=True)
            # self.post_save(self.object, created=True)
            # headers = self.get_success_headers(serializer.data)
            # serializer = TicketSerializer(serializer.object)
            serializer.save(course_code= school_course,
                            school_id= school)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

