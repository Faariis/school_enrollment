from django.urls import path
from .views import RegisterView, LoginView, TeacherView, LogoutView, ApiOverview
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', ApiOverview.as_view(), name='teacher-home'),
    path('loginold',  LoginView.as_view()),
    path('register',  RegisterView.as_view()),
    path('teacher', TeacherView.as_view()),
    path('logout', LogoutView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
