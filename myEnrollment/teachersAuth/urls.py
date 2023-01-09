from django.urls import path
from teachersAuth.api.views import (
    ApiOverview,
    LogoutView
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
]   
