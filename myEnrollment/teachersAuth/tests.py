from django.test import TestCase

# Create your tests here.
# test filename should be be test_<>.py
# methods should start with test_<name> 

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
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
  
    self.teacher= Teacher.objects.create_user(email="a@a", password="a",
                                              first_name='Anel', last_name= 'Husakovic',
                                              is_superuser= 1,
                                              is_staff=1,
                                              school_id=self.school_tscsa,
                                              course_code=self.course_rtia)
    for t in Teacher.objects.all():
      t.set_password(t.password)
      t.save()
    #self.token= Token.objects.get(user__username= self.teacher)
    #self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
  def log_me_with_jwt(self):
    jwt= self.test_login()
    token= jwt.data['access']
    print('jwt data: ', token)
    self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
  
  def test_login(self):
    """
    Ensure we can create new JWT token
    """

    url= reverse('token_obtain_pair')
    data= {
            "email": "a@a",
            "password": "a"
          }
    # self.teacher.is_active= True #False doesn't affect
    self.teacher.is_active= False # this deosn't affect
    self.teacher.save()
    print("is active: " , self.teacher.is_active)
    resp= self.client.post(url, data,format='json')

    self.assertEqual(resp.status_code, status.HTTP_200_OK,
                     resp.data)
    return resp
    # To execute: `./manage.py test`
    #self.assertTrue('token' in resp.data)
    #token = resp.data['token']

  def test_get_cantons(self):
    self.log_me_with_jwt()
    resp= self.client.get(reverse('canton-list'), data={'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_200_OK,
                     resp.data)
    self.assertEqual(Canton.objects.count(), 2)

  def test_get_canton_by_canton_code(self):
    self.log_me_with_jwt()
    resp= self.client.get(reverse('canton-detail', args=('zdk',)), data={'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_200_OK,
                     resp.data)

  def test_create_canton_by_canton_code(self):
    self.log_me_with_jwt()
    data={
      'format': 'json',
      '_canton_code':'tz',
      'canton_name':"Tuzlanski kanton"
    }
    resp= self.client.post(reverse('canton-detail', args=('tz',)), data)
    self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                     resp.data)
    # Put should change from null to value (as done in postman), but it is not
    resp= self.client.put(reverse('canton-detail', args=('tz',)), data)
    self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND,
                     resp.data)

    #TODO: move testing to application secondarySchools and finish for schools
