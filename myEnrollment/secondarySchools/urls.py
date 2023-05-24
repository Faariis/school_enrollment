from django.urls import path
from secondarySchools.api.views import (
                                        CantonView,
                                        CantonDetailView,
                                        CantonSchoolView,
                                        CantonSchoolDetailView,
                                        SchoolView,
                                        SchoolViewDetail,
                                        SchoolCoursesListView,
                                        SchoolCoursesCreateView,
                                       )

urlpatterns = [
    path('canton/', CantonView.as_view(), name="canton-list"),
    path('canton/<str:_canton_code>/', CantonDetailView.as_view(), name="canton-detail"),

    path('canton/schools/<str:canton_code>/', CantonSchoolView.as_view(), name="canton-school-list"),
    path('canton/schools/<int:pk>/', CantonSchoolDetailView.as_view(), name="canton-school-detail"),
    
    path('school-list/', SchoolView.as_view(), name="school-list"),
    path('school-list/<int:pk>/', SchoolViewDetail.as_view(), name="school-detail"),
    path('school-list/<int:pk>/course-create/', SchoolCoursesCreateView.as_view(), name="school-course-create"),
    path('school-list/<int:pk>/courses/', SchoolCoursesListView.as_view(), name="school-course-list"),

    # path('school-list/<int:pk>/', TeacherLoginView.as_view(), name="teacher-list"),
    # path('teachers/', TeachersList.as_view(), name="teachers-info"),
    # # path('schools/<int:pk>', SchoolView.as_view(), name='secondarySchools-detail')
    # path("teacherlist/", TeachersList2.as_view(), name="teacher-list2")
]
