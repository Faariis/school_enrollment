from django.urls import path
from teachersAuth.api.views import (
    ApiOverview,
    LogoutView,
    TeacherCreateView,
    TeacherViewDetail,
    TeacherList,
    VerifyEmailView,
    LoginTeacherView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', ApiOverview.as_view(), name='teacher-home'),
    path('login/', LoginTeacherView.as_view(), name='login-teacher'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('teacher-create/', TeacherCreateView.as_view(), name= 'teacher-create'),
    path('teacher/<int:pk>/', TeacherViewDetail.as_view(), name='teacher-detail'),
    path('teacher-list/', TeacherList.as_view(), name='teacher-list'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
]   
