from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Teacher
# # Register your models here.
# class CustomUserAdmin(UserAdmin):
#     ordering = ('email',)

# admin.site.register(Teacher, CustomUserAdmin)
# ... and, since we're not using Django's built-in permissions,
# # unregister the Group model from admin.
# admin.site.unregister(Group)