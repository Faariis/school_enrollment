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
from rest_framework.generics import (
                                      CreateAPIView,
                                      RetrieveUpdateDestroyAPIView,
                                      ListAPIView
                                    )
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from teachersAuth.serializers import (
                                       TeacherSerializer,
                                       TeacherSerializerUpdate,
                                       TeacherSerializerList,
                                       EmailVerificationSerializer
                                     )
from teachersAuth.models import Teacher
from secondarySchools.models import SecondarySchool,CoursesSecondarySchool

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings as api_settings
import jwt
from django.contrib.auth.hashers import make_password

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
            'GET/PUT/DELETE new teacher':'/api/teacher/<pk>/',
            'GET teacher list - visible to admin only':'/api/teacher-list/',
            
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
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            serializer.validated_data['password']=make_password(password)
            # self.pre_save(serializer.object)
            # self.object = serializer.save(force_insert=True)
            # self.post_save(self.object, created=True)
            # headers = self.get_success_headers(serializer.data)
            # serializer = TicketSerializer(serializer.object)
            serializer.save(course_code= school_course,
                            school_id= school)

            # ----- Verify the user by sending the access token to that user, so he needs to verify ----
            user_mail= serializer.data['email']
            user= Teacher.objects.get(email= user_mail)
            subject_mail= 'Verify email'
            protocol= 'http://'
            domain= get_current_site(request).domain
            relative_link= reverse('email-verify')
            refresh_token= RefreshToken.for_user(user)
            # register token
            access_token= str(refresh_token.access_token)
            absurl=protocol+domain+relative_link+"?token="+access_token
            msg="Hi please verify your email: \n" + \
                "domain: "+ domain + "\n"+\
                "relative: "+ relative_link + "\n"+ \
                "token: "+ str(access_token) + "\n" + \
            "\n Verification valid 2 days. This mail is autogenerated. Don't respond."
            msg= "Hi verify: \n"+absurl
            # information from api_settings.SIMPLE_JWT.ACCESS_TOKEN_LIFETIME (have to export DJANGO_SETTINGS_MODULE= myEnrollmentDB.settings)
            # It will go to user email directly
            Teacher.email_user(user, subject=subject_mail, message=msg)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherViewDetail(RetrieveUpdateDestroyAPIView):
    serializer_class= TeacherSerializerUpdate
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return Teacher.objects.all()

    # Make sure that normal users can get only current form to update
    def get(self, request, *args, **kwargs):
        pk= self.kwargs['pk']
        t_id= request.user.id
        if pk != t_id and t_id:
            teacher= Teacher.objects.get(id= t_id)
            if teacher.is_superuser == False:
                return Response({'message':'user not authirized to view teacher'},
                       status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return super().get(request, *args, **kwargs)

class TeacherList(ListAPIView):
    queryset= Teacher.objects.all()
    serializer_class= TeacherSerializerList

    def list(self, request):
        if Teacher.objects.get(id= request.user.id).is_superuser:
            qs= self.get_queryset()
            serializer= self.serializer_class(qs, many= True)
            return Response(serializer.data)


# from https://www.youtube.com/watch?v=cdg48zsjZAE
# https://github.com/CryceTruly/incomeexpensesapi/tree/master/authentication
class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token= request.GET.get('token')
        try:
            payload= jwt.decode(jwt=token, key= api_settings.SECRET_KEY, algorithms=['HS256'])
            teacher= Teacher.objects.get(id= payload['user_id'])
            if  not teacher.is_verified:
                teacher.is_verified= True
                teacher.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
