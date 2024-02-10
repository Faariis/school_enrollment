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
from django.contrib.auth import get_user_model # Used in the verification
import jwt
from datetime import datetime, timedelta
from django.conf import settings

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
    """
    We need school_id, _course_code in order to make right request,
    instead we will get 400 (Bad request)
    """
    self.testData= {
      "email": "profesor@test.com",
      "password": "123456789",
      "school_id": self.school_tscsa.id,
      "course_code": self.course_rtia._course_code,
      "first_name": "Niko",
      "last_name": "Nikic",
    }

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

  """
  TESTS BEGIN HERE
  """

  """
  Route 1: `/api/teachers/teacher-list/`
  Options: GET - visible to admins only
  """
  def test_get_teacher_list(self):
    """
    GET: Test getting teachers (200);
    Note: This test is for superusers only!
    Route: `/api/teachers/teacher-list/`
    """
    self.log_me_with_jwt()
    url= reverse('teacher-list')
    resp= self.client.get(url, data= {'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
    print("\nUrl: " + url + " - Super user succesfully got the list.")


  def test_get_teacher_list_is_not_superuser(self):
    """
    GET: Test getting teachers (203);
    If teacher is regular user (not a superuser)
    authorization should fail for current teacher to get the list;
    """
    self.teacher.is_superuser= 0
    self.log_me_with_jwt()
    url= reverse('teacher-list')
    resp= self.client.get(url, data= {'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                     resp.data)
    actual_message= resp.data['message']
    expected_message= '''Teacher not authorized to view teacher.'''
    self.assertRegex(actual_message, expected_message)
    print("\nUrl: " + url + " - Teacher is not a authorized to get the list.")
    self.teacher.is_superuser= 1


  """
  Route 2: `/api/teachers/teacher/<pk>/`
  Options: GET/PUT/DELETE
  """
  def test_get_teacher_teacher_detail(self):
    """
    GET: Test getting teacher with specific id (200);
    Route: `/api/teachers/teacher/<pk>/`
    """
    self.log_me_with_jwt()
    print("Test superuser ", self.teacher.is_superuser)
    url= reverse('teacher-detail', args= (self.teacher.id,))
    resp= self.client.get(url, data= {'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
    print("\nUrl: " + url + " - Succesfully got the teacher with specific id.")


  def test_get_teacher_teacher_detail_is_not_superuser(self):
    """
    GET: Test getting teacher with specific id (200);
    If teacher is regular user (not a superuser), test should pass;
    Route: `/api/teachers/teacher/<pk>/`
    """
    self.teacher.is_superuser= 0
    self.log_me_with_jwt()
    print("Test superuser ", self.teacher.is_superuser)
    url= reverse('teacher-detail', args= (self.teacher.id,))
    resp= self.client.get(url, data= {'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
    print("\nUrl: " + url + " - Succesfully got the teacher with specific id.")
    self.teacher.is_superuser= 1


  def test_get_teacher_teacher_detail_not_exists(self):
    """
    GET: Test getting teacher with non-existing id (404);
    Route: `/api/teachers/teacher/<pk>/`
    Testing with id value 100;
    """
    self.log_me_with_jwt()
    url= reverse('teacher-detail', args= (100,))
    resp= self.client.get(url, data= {'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND, resp.data)
    print("\nUrl: " + url + " - Cannot get teacher, Id= 100 does not exist.")


  def test_create_teacher_teacher_detail(self):
    """
    POST: Test shouldn't be allowed (405)
    """
    self.log_me_with_jwt()
    url= reverse('teacher-detail', args= [self.teacher.id])
    data= self.testData
    # We need to create data instead we will get 400 (Bad request)
    resp= self.client.post(url, data)
    self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                      resp.data)
    print("\nUrl: " + url + " - POST method is not allowed.")


  def test_update_teacher_teacher_detail(self):
    """
    UPDATE: Test updating teacher with specific id (200);
    Note: Not passing the password in the data;
    """
    self.log_me_with_jwt()
    url= reverse('teacher-detail', args= (self.teacher.id,))
    """
    We didn't updated `school_id` and `_course_code`, since they are FK.
    Also password is not updated, it needs to be hashed;
    We need data in order to make right request, instead we will get 400
    (Bad request)
    """
    data= {
      "email": "profesor@test.com",
      "school_id": self.school_tscsa.id,
      "course_code": self.course_rtia._course_code,
      "first_name": "Niko",
      "last_name": "Nikic",
    }
    resp= self.client.put(url, data)
    self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
    self.teacher.refresh_from_db()
    self.assertEqual(self.teacher.email, self.testData['email'])
    self.assertEqual(self.teacher.first_name, self.testData['first_name'])
    self.assertEqual(self.teacher.last_name, self.testData['last_name'])
    print("\nUrl: " + url + " - Succesfully updated teacher.")


  def test_update_teacher_teacher_detail_id_not_exists(self):
    """
    UPDATE: Test updating teacher with non-existing id (404);
    Testing with id value 100;
    """
    self.log_me_with_jwt()
    url= reverse('teacher-detail', args= [100])
    """
    We need data in order to make right request, instead we will get 400
    (Bad request).
    """
    data= self.testData
    resp= self.client.put(url, data)
    self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND,
                    resp.data)
    print("\nUrl: " + url + " - Cannot update teacher, Id= 100 does not exist.")


  def test_delete_teacher_teacher_detail(self):
    """
    DELETE: Test deleting teacher with specific id (204);
    """
    self.log_me_with_jwt()
    url= reverse('teacher-detail', args= [self.teacher.id])
    resp= self.client.delete(url)
    self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT, resp.data)
    try:
      self.teacher.refresh_from_db()
    except Teacher.DoesNotExist:
      """
      This case occurs if there is single teacher in DB, as we currently have.
      """
      deleted_teacher= None
      try:
        deleted_teacher= Teacher.objects.get(id= self.teacher.id)
      except Teacher.DoesNotExist:
        self.assertIsNone(deleted_teacher)
        print("\nUrl: " + url + " - Succesfully deleted teacher.")


  def test_delete_teacher_teacher_detail_not_exists(self):
    """
    DELETE: Test deleting teacher with non-existing id (404);
    Testing with id value 100;
    """
    self.log_me_with_jwt()
    url= reverse('teacher-detail', args= [100])
    resp= self.client.delete(url)
    self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND, resp.data)
    print("\nUrl: " + url + " - Cannot delete teacher, Id= 100 does not exist.")


  """
  Route 3: `/api/teachers/teacher-create/`
  Options: POST - admin can create a new teacher
  """
  def test_create_teacher_teacher_create(self):
    """
    POST: Test creating teacher (201);
    """
    self.log_me_with_jwt()
    """
    Counts the number of teachers before creating a new one;
    """
    teacher_count= Teacher.objects.count()
    url= reverse('teacher-create')
    """
    Creating a new teacher using testData;
    """
    data= self.testData
    resp= self.client.post(url, data)
    self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
    """
    Counting the number of teachers;
    Compares the number of teachers before and after client.post();
    """
    self.assertEqual(Teacher.objects.count(), teacher_count+1)
    print("\nUrl: " + url + " - Succesfully created a new teacher.")


  def test_create_teacher_teacher_create_school_id_not_exist(self):
    """
    POST: Test creating teacher but school_id does not exist (400);
    School_id value is 100;
    """
    self.log_me_with_jwt()
    url= reverse('teacher-create')
    data= {
        "email": "profesor2@test.com",
        "password": "123456789",
        "school_id": 100,
        "course_code": self.course_rtia._course_code,
        "first_name": "Osoba",
        "last_name": "Tri",
            }
    resp= self.client.post(url, data)
    self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.data)
    """
    Checks if the response data error is 'wrong school';
    """
    errorMessage= 'wrong school'
    self.assertEqual(resp.data['error'], errorMessage)
    print("\nUrl: " + url + " - School id 100 does not exist.")


  def test_put_teacher_teacher_create(self):
    """
    UPDATE: Test shouldn't be allowed (405);
    """
    self.log_me_with_jwt()
    url= reverse('teacher-create')
    """
    Even if we pass the data updating is not allowed;
    """
    data= self.testData
    resp= self.client.put(url, data)
    self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                      resp.data)
    print("\nUrl: " + url + " - PUT method is not allowed.")


  """
  Route 4: `/api/teachers/login/`
  Teacher login;
  We already have a (200), but we are testing (401);
  """
  def test_login_unauthorized(self):
    """
    Unauthorized/unsuccessful login (401);
    When there is no JWT token;
    When credentials are invalid;
    """
    self.log_me_with_jwt()
    url= reverse('token_obtain_pair')
    data= {'email': "profesor@test.com", 'password': "123456789"}
    resp= self.client.post(url, data, format= 'json')
    self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    print("\nUrl: " + url + " - Unauthorized login, invalid credentials.")


  """
  Route 5: `/api/teachers/logout/`
  Teacher logout;
  """
  def test_logout_successful(self):
    """
    Successful logout (200);
    """
    self.log_me_with_jwt()
    url= reverse('logout')
    resp= self.client.post(url)
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    self.assertNotIn('JWT', resp.cookies)
    """
    Checks if the message key exists in the data response;
    Checks if the message is 'success';
    """
    message= resp.data.get('message', None)
    self.assertEqual(message, 'success')
    print("\nUrl: " + url + " - Successful logout.")


  def test_logout_unauthorized(self):
    """
    Unauthorized/Unsuccessful logout (401);
    Missing JWT;
    """
    url= reverse('logout')
    resp= self.client.post(url)
    self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertNotIn('JWT', resp.cookies)
    print("\nUrl: " + url + " - Unauthorized logout attempt without JWT.")


  """
  Route 6: `/api/teachers/email-verifiy/`
  Email verification;
  """
  def test_email_verification_successful(self):
    """
    Authorized/successful email verification;
    """
    self.log_me_with_jwt()
    user= get_user_model().objects.get(email= "a@a")
    refresh_token= RefreshToken.for_user(user)
    access_token= str(refresh_token.access_token)
    url= f"{reverse('email-verify')}?token={access_token}"
    resp= self.client.get(url, format= 'json')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    """
    Checks if response data contains email;
    Checks if the email value is 'Successfully activated';
    """
    self.assertIn('email', resp.data)
    self.assertEqual(resp.data['email'], 'Successfully activated')
    print("\nUrl: " + url + " - Successful email verification.")


  def test_email_verification_unauthorized(self):
    """
    Unauthorized/unsuccessful email verification (401);
    Incorrect/missing JWTs;
    """
    user= get_user_model().objects.get(email= "a@a")
    refresh_token= RefreshToken.for_user(user)
    access_token= str(refresh_token.access_token)
    url= f"{reverse('email-verify')}?token= {access_token}"
    resp= self.client.get(url, format= 'json')
    self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    print("\nUrl: " + url + " - Unauthorized email verification.")


  def test_email_verification_invalid_token(self):
    """
    Missing token or invalid token (400);
    """
    self.log_me_with_jwt()
    url= f"{reverse('email-verify')}?token= invalid"
    resp= self.client.get(url, format= 'json')
    self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    """
    Checks if the response data error is 'Invalid token';
    """
    self.assertEqual(resp.data['error'], 'Invalid token')
    print("\nUrl: " + url + " - Invalid email verification token.")


  def test_email_verification_expired_token(self):
    """
    Unsuccessful email verification (400);
    Expired token provided;
    """
    self.log_me_with_jwt()
    """
    Creating an expired JWT token using jwt.encode;
    It takes 3 arguments: user_id, expiration time (15 hours) and a secret key;
    The secret key signs the token and the HS256 is the algorithm.
    """
    expired_token= jwt.encode({'user_id': 1, 'exp': datetime.utcnow()
                              - timedelta(hours= 15)},
                                settings.SECRET_KEY, algorithm= 'HS256')
    url= f"{reverse('email-verify')}?token={expired_token}"
    resp= self.client.get(url, format= 'json')
    self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    """
    Checks if the response data error is 'Activation expired';
    """
    self.assertEqual(resp.data['error'], 'Activation Expired')
    print("\nUrl: " + url + " - Expired email verification token.")


  """
  Route 7: `/api/teachers/login/refresh/`
  Login refresh;
  """
  def test_token_refresh_successful(self):
    """
    Successful refreshing of a JWT access token (200).
    """
    jwt= self.test_login()
    refresh_token= jwt.data['refresh']
    url= reverse('token_refresh')
    data= {'refresh': refresh_token}
    resp= self.client.post(url, data, format= 'json')
    self.assertEqual(resp.status_code, status.HTTP_200_OK)
    self.assertIn('access', resp.data)
    print("\nUrl: " + url + " - Successful refreshing access token.")


  def test_token_refresh_unauthorized(self):
    """
    Unauthorized/unccessful refreshing of a JWT access token (401).
    """
    refresh_token= "Invalid token"
    url= reverse('token_refresh')
    data= {'refresh': refresh_token}
    resp= self.client.post(url, data, format= 'json')
    self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
    print("\nUrl: " + url + " - Unsuccessful refreshing access token.")

