import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str
from django.utils.translation import ugettext, ugettext_lazy as _
# https://stackoverflow.com/questions/71420362/django4-0-importerror-cannot-import-name-ugettext-lazy-from-django-utils-tra
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

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

def get_teacher_id_from_jwt(request, jwt_name='jwt'):
    # get cookie and from cookie retrieve the user
    token = request.COOKIES.get(str(jwt_name))
    # decode it to get the user
    if not token:
        raise AuthenticationFailed("Unauthenticated access")
    try:
        payload= jwt.decode(token, api_settings.JWT_PRIVATE_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated access")
    teacher= Teacher.objects.get(id= payload['id'])
    return teacher

class TeacherLoginView(RetrieveAPIView):
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (AllowAny,)
    lookup_field = "id"
    queryset=Teacher.objects.all()
    serializer_class = TeacherLoginSerializer
    def get(self, request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)
        status_code = status.HTTP_200_OK
        response={
            'success':'True',
            'status_code': status_code,
            'message': 'Teacher logged in  successfully',
            'token' : serializer.data['jwt_token'],
        }
        return Response(response, status= status_code)

class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response
