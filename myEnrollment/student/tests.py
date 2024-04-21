# Create your tests here.
# test filename should be be test_<>.py
# methods should start with test_<name>

from datetime import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from teachersAuth.models import Teacher
from secondarySchools.models import (
                                      SecondarySchool,
                                      CoursesSecondarySchool,
                                      Canton
                                    )
from student.models import (
                             Pupil,
                             Class,
                             PupilClassesAcknowledgments,
                           )
import json

"""
I kept the registration because there are other views that need admin permission;
Currently PupilClassesAcknowledgments is AllowAny;
"""
class RegisterTestCase(APITestCase):
  # We are making registration
  # In order to run the test, we must register user first.
  def setUp(self):
    # General settings
    self.email= "a@a"
    self.password= "a"
    self.name= "Anel"
    self.last_name= "Husakovic"

    self.canton_sa= Canton(_canton_code= "SA",
                   canton_name= "Sarajevski kanton")
    self.canton_sa.save()

    self.school_tscsa= SecondarySchool(school_canton_code= self.canton_sa,
                                       school_name= "Tehnicka skola",
                                       school_address="Dobrinja")
    self.school_tscsa.save()

    self.course_rtia= CoursesSecondarySchool(_course_code="RTiA",
                                   course_name= "Racunarska tehnika i automatika",
                                   school_id= self.school_tscsa)
    self.course_rtia.save()

    self.class_eight= Class(_classes= 'VIII')
    self.class_eight.save()

    self.class_nine= Class(_classes= 'IX')
    self.class_nine.save()

    self.pupil= Pupil(
            id= 1,
            primary_school= 'Mak Dizdar',
            secondary_shool_id= self.school_tscsa,
            desired_course_A= self.course_rtia,
            name= 'John',
            last_name= 'Doe',
            gender= 'Male',
            address= 'Crkvice',
            guardian_name= 'Jill',
            phone_number= '1234567890',
            guardian_number= '9876543210',
            guardian_email= 'Jill@mail.com',
            email= 'John@mail.com',
            special_case= 'regular',
            acknowledgment= None
        )
    self.pupil.save()

    self.acknowledgment = PupilClassesAcknowledgments(
            pupil_id= self.pupil,
            ack_name= 'Matematika',
            ack_points= 5,
            ack_position= 1,
            ack_level= 'Federalno',
            ack_class_id= self.class_eight
        )
    self.acknowledgment.save()

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


  def log_me_with_jwt(self):
    """
    Base function for logging with JWT
    1) tests login with `test_login()` on route `api/teachers/login`
    2) uses returned JWT access data to make authorization
    """
    url= reverse('token_obtain_pair')
    data = {'email': self.email, 'password': self.password}
    self.teacher.is_active= True # False will return 401 response
    self.teacher.save()
    resp= self.client.post(url, data, format='json')
    self.assertEqual(resp.status_code, status.HTTP_200_OK,
                     resp.data)
    token= resp.data['access']
    self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))


  """
  TESTS BEGIN HERE
  """
  """
  Route 1: `student/<int:pk>/acknowledgments/`
  Options: GET/POST
  """
  def test_get_pupil_acknowledgments(self):
    """
    GET: Test getting acknowledgment for pupil with specific id (200);
    """
    url = reverse('pupil-class-acknowledgment', args= (self.pupil.id,))
    resp = self.client.get(url, data= {'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
    print("\nUrl: " + url + " - Succesfully got the acknowledgment of the pupil.")
    # Print the response content to the console
    print(resp.data)


  def test_get_pupil_acknowledgments_not_exist(self):
    """
    GET: Test getting acknowledgment for pupil that does not exist (404);
    Pupil_id value is 100;
    """
    url = reverse('pupil-class-acknowledgment', args= (100,))
    resp = self.client.get(url, data= {'format': 'json'})
    self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND, resp.data)
    print("\nUrl: " + url + " - Can't get acknowledgment, Pupil_id 100 does not exist.")


  def test_create_pupil_acknowledgment(self):
    """
    POST: Test creating acknowledgment for a pupil (201);
    """
    acknowledgment_count= PupilClassesAcknowledgments.objects.count()
    url = reverse('pupil-class-acknowledgment', args= (self.pupil.id,))
    data = {
        'ack_name': 'Matematika',
        'ack_position': 1,
        'ack_level': 'Federalno',
        'pupil_id': self.pupil.id,
        'ack_class_id': self.class_nine._classes,
        }
    resp= self.client.post(url, data)
    self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
    """
    Counting the number of acknowledgments;
    Compares the number of acknowledgments before and after client.post();
    """
    self.assertEqual(PupilClassesAcknowledgments.objects.count(), acknowledgment_count+1)
    print("\nUrl: " + url + " - Successfully created acknowledgment for the pupil.")


  def test_create_pupil_acknowledgment_not_exist(self):
    """
    POST: Test creating acknowledgment for a pupil that does not exist (400);
    Pupil_id values is 100;
    """
    url = reverse('pupil-class-acknowledgment', args= (self.pupil.id,))
    data = {
        'ack_name': 'Matematika',
        'ack_position': 1,
        'ack_level': 'Federalno',
        'pupil_id': 100,
        'ack_class_id': self.class_nine._classes,
        }
    resp= self.client.post(url, data)
    self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.data)
    print("\nUrl: " + url + " - Can't create acknowledgment, Pupil_id 100 does not exist.")