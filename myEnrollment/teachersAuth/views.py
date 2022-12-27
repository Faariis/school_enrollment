from django.shortcuts import render
from rest_framework.views import APIView, Response
from .serializers import TeacherSerializer

# Create your views here.
class RegisterView(APIView):
    # get and post function in APIView
    def post(self, request):
        # To create the user first create serializer.py 
        serializer= TeacherSerializer(data= request.data)
        serializer.is_valid( raise_exception= True)
        serializer.save()
        # return it, to test it install postman
        return Response(serializer.data)
        # pass


