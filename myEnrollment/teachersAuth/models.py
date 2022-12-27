from django.db import models
# Followed the tutorial https://www.youtube.com/watch?v=PUzgZrS_piQ&list=PLlameCF3cMEu-LbsQYUDUVkiZ2jc2rpLx
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Teacher(AbstractUser):
    name= models.CharField(max_length = 50)
    email= models.CharField(max_length = 50, unique= True)
    password= models.CharField(max_length = 255)
    # Django by default creates username we have to overrdie it
    # We want that Django logs in with email and password
    username= None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []