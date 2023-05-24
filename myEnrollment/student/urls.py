from django.urls import path
from student.api.views import (
    ApiOverview,
    )


urlpatterns = [
    path('', ApiOverview.as_view(), name='teacher-home'),
]   
