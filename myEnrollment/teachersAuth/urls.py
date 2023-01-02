from django.urls import path
from .views import RegisterView, LoginView, TeacherView, LogoutView
urlpatterns = [
    path('login',  LoginView.as_view()),
    path('register',  RegisterView.as_view()),
    path('teacher', TeacherView.as_view()),
    path('logout', LogoutView.as_view()),
]
