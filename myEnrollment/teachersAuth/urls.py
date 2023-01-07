from django.urls import path
from .views import (
    ApiOverview,
    TeacherLoginView,
    TeachersList,
    TeachersList2,
    LogoutView,
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', ApiOverview.as_view(), name='teacher-home'),
    path('teacher/', TeacherLoginView.as_view(), name="teacher-info"),
    path('teachers/', TeachersList.as_view(), name="teachers-info"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('schools/<int:pk>', SchoolView.as_view(), name='secondarySchools-detail')
    path("teacherlist/", TeachersList2.as_view(), name="teacher-list2")
]   
