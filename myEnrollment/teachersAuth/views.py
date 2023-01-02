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

# Create your views here.
class RegisterView(APIView):
    # get and post function in APIView
    def get(self, request):
        teacher= get_teacher_id_from_jwt(request, 'jwt')
        if teacher.is_superuser == 0:
            return Response({"message": "Current user is not super user. Registration not allowed!"})
        print("GET: ", teacher)

        # It should show all teaches from database to delete/update
        teachers= Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        current_user = request.user
        # if current_user.is_authenticated:
        #     # Registration can be done only by super admin
        #     if current_user.is_superuser == 0:
        #         return Response({"message": "Current user is not super user. Registration not allowed!"})
        # else:
        #     return Response({"message": "AnonymousUser not allowed!"})
        teacher= get_teacher_id_from_jwt(request, 'jwt')
        print(teacher)
        if teacher.is_superuser == 0:
            return Response({"message": "Current user is not super user. Registration not allowed!"})
        # Here we know current_user is super user and can proceed
        # To create the user first create serializer.py 
        serializer= TeacherSerializer(data= request.data)
        serializer.is_valid( raise_exception= True)
        serializer.save()
        # return it, to test it install postman
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        # Handle anonymous use - not needed, all authentication will be done on frontend
        email= request.data['email']
        password= request.data['password']

        # teacher= Teacher.objects.get(email= email, password= password)
        # Since email is unique
        teacher= Teacher.objects.filter(email= email).first()
        #teacher= Teacher.objects.get(email= email) < returns single instance only
        if teacher is None:
            raise AuthenticationFailed('User not found!')
        
        # This function is also provided by djanog
        if not teacher.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        # Payload is set of claims
        payload= {
            'id': teacher.id,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }
        # secret can be as env var or can be in payload
        # no need for .decode('utf-8')
        token= jwt.encode(payload, api_settings.JWT_PRIVATE_KEY, algorithm="HS256")
        update_last_and_previous_login(None, teacher)
        response= Response()
        # We don't want frontend to access token so httponly
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data= {
            'jwt':token
        }
        return response

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
