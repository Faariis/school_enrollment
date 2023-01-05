from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import TeacherSerializer
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

class TeacherView(APIView):
    def get(self, request):
        teacher= get_teacher_id_from_jwt(request, 'jwt')
        serializer= TeacherSerializer(teacher)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response
