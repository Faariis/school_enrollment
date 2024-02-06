from django.test import TestCase

# Create your tests here.
# test filename should be be test_<>.py
# methods should start with test_<name> 

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from teachersAuth.models import Teacher
from secondarySchools.models import (
                                      SecondarySchool,
                                      CoursesSecondarySchool,
                                      Canton
                                    )
# from django.contrib.auth import get_user_model
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterTestCase(APITestCase):
  # We are making registration 
  # In order to run the test, we must register user first.
  def setUp(self):
    # General settings
    self.email= "a@a"
    self.password= "a"
    self.name= "Anel"
    self.last_name= "Husakovic"

    """
    Workflow:
    1) Create canton
    2) Create school in canton
    3) Create course in school
    4) Create teacher in school with course (school is redundant @TODO)
    PURPOSE: Test teacher routes only !!!
    """
    self.canton_sa= Canton(_canton_code= "SA",
                   canton_name= "Sarajevski kanton")
    self.canton_sa.save()

    self.canton_zdk= Canton(_canton_code= "zdk",
                   canton_name= "Zenicko-dobojski kanton")
    self.canton_zdk.save()

    self.school_tscsa= SecondarySchool(school_canton_code= self.canton_sa,
                                       school_name= "Tehnicka skola",
                                       school_address="Dobrinja")
    self.school_tscsa.save()
    
    self.course_rtia= CoursesSecondarySchool(_course_code="RTiA", 
                                   course_name= "Racunarska tehnika i automatika",
                                   school_id= self.school_tscsa)
    self.course_rtia.save()
  
    self.teacher= Teacher.objects.create_user(email= self.email,
                                              password= self.password,
                                              first_name= self.name,
                                              last_name= self.last_name,
                                              is_superuser= 1,
                                              is_staff= 1,
                                              school_id= self.school_tscsa,
                                              course_code= self.course_rtia)
    for t in Teacher.objects.all():
      t.set_password(t.password)
      t.save()
      print ("Teacher: "+ t.get_short_name() + " password set!")


    #self.token= Token.objects.get(user__username= self.teacher)
    #self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
  def log_me_with_jwt(self):
    """
    Base function for logging with JWT
    1) tests login with `test_login()` on route `api/teachers/login`
    2) uses returned JWT access data to make authorization
    """
    jwt= self.test_login()
    token= jwt.data['access']
    print('jwt data: ', token)
    self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))


  def test_login(self):
    """
    Ensure we can create new JWT token from `api/teachers/login`
    """
    url= reverse('token_obtain_pair')
    data = {'email': self.email, 'password': self.password}
    self.teacher.is_active= True # False will return 401 response
    self.teacher.save()
    resp= self.client.post(url, data, format='json')
    print("\nUrl: " + url + "\nResponse from test_login: ", resp)
    self.assertEqual(resp.status_code, status.HTTP_200_OK,
                     resp.data)
    return resp
    # To execute: `./manage.py test`
    #self.assertTrue('token' in resp.data)
    #token = resp.data['token']
  
  # TODO go through all teachers route (see teachersAuth.urls.py)
  # TODO and apply all operations per specific route
