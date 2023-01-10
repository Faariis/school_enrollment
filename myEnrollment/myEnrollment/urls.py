"""myEnrollment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="School Enrollment Application for Bosnia & Herzegovina",
      default_version='v1',
      description="Transparent enrollment of students in secondary schools and faculties",
      terms_of_service="https://www.myap.com/policies/terms/",
      contact=openapi.Contact(email="info@eacon.ba"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include `urls` file from application
    # to accept all end-points of user
    path('api/', include('teachersAuth.urls')),
    path('api/', include('secondarySchools.urls')),
    #path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

