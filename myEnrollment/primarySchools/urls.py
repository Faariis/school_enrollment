from django.urls import path
from primarySchools.api.views import (
    ApiOverview,
    )


urlpatterns = [
    path('', ApiOverview.as_view(), name='teacher-home'),
]   
