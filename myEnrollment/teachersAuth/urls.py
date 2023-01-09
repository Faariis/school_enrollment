from django.urls import path
from .views import (
    ApiOverview,
    TeacherView,
    LogoutView,
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', ApiOverview.as_view(), name='teacher-home'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('school-list/', TeacherView.as_view(), name="teacher-list"),
    # path('school-list/<int:pk>/', TeacherLoginView.as_view(), name="teacher-list"),
    # path('teachers/', TeachersList.as_view(), name="teachers-info"),
    # # path('schools/<int:pk>', SchoolView.as_view(), name='secondarySchools-detail')
    # path("teacherlist/", TeachersList2.as_view(), name="teacher-list2")
]   
