from django.urls import path
from student.api.views import (
    ApiOverview,
    PupilCreateView,
    PupilView,
    PupilViewDetail,
    PupilCoursesView,
    PupilCoursesDetailView)


urlpatterns = [
    path('student-list/', PupilView.as_view(), name='student-list'), # get/create new student
    path('student-list/<int:pk>/', PupilViewDetail.as_view(), name="student-detail"), # edit/update/delete studen with id
    path('student-list/<int:pk>/course-create/', PupilCoursesView.as_view(), name="student-course-create"), #get/create new course of a class
    path('student-list/<int:pk>/courses/', PupilCoursesDetailView.as_view(), name="student-course-detail"), #get/create new course of a class
]
