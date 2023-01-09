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

class LogoutView(APIView):
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data= {
            'message':'success'
        }
        return response
