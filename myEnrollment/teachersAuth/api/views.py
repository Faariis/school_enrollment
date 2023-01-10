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
                                      ListAPIView,
                                      GenericAPIView
                                    )
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from teachersAuth.serializers import (
                                       TeacherSerializer,
                                       TeacherSerializerUpdate,
                                       TeacherSerializerList,
                                       TeacherPasswordResetSerializer,
                                       SetNewPasswordSerializer
                                     )
from teachersAuth.models import Teacher

from secondarySchools.models import SecondarySchool,CoursesSecondarySchool

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from teachersAuth.utils import Util
from django.shortcuts import redirect


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


class TeacherPasswordReset(GenericAPIView):
    serializer_class= TeacherPasswordResetSerializer
    def post(self, request):
        data={'data':request.data,'request': request}
        serializer= self.serializer_class(data=data)
        email= request.data['email']
        # Check if email exists
        if Teacher.objects.filter(email= email).exists():
            teacher= Teacher.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(teacher.id))
            token = PasswordResetTokenGenerator().make_token(teacher)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': teacher.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Teacher.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


# From here https://www.youtube.com/watch?v=2kKwPk5qPUs
class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
