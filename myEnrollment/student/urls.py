from django.urls import path
from student.api.views import (
    ApiOverview,
    PupilCreateView,
    PupilView,
    PupilViewDetail,
    PupilCoursesView,
    PupilCoursesDetailView,
    PupilClassCourseView,
    PupilClassAcknowledgmentView,
    PupilAverageGradeView,
    SpecialCourseGradesView,

    TotalAcknowledgmentPointsView,
    #TotalPointsSummaryView,
    TotalPointsSummaryByCourseCodeView,
    TotalPointsSummaryViewPerName,
    )


urlpatterns = [
    path('student-list/', PupilView.as_view(), name='student-list'), # get/create new student
    path('student-list/<int:pk>/', PupilViewDetail.as_view(), name="student-detail"), # edit/update/delete studen with id
    path('student-list/<int:pk>/course-create/', PupilCoursesView.as_view(), name="student-course-create"), #get/create new course of a class
    path('student-list/<int:pk>/courses/', PupilCoursesDetailView.as_view(), name="student-course-detail"), #get/create new course of a class
    path('student/class_course/', PupilClassCourseView.as_view(), name="pupil-class-course"),
    # Returns and posts the acknowledgments;
    path('student/<int:pk>/acknowledgments/', PupilClassAcknowledgmentView.as_view(), name="pupil-class-acknowledgment"),
    # Calculates the acknowledgment points;
    path('student/<int:pk>/acknowledgmentsPoints/', TotalAcknowledgmentPointsView.as_view(), name="pupil-class-acknowledgment_points"),
    # Calculates the average grades;
    path('student/<int:pk>/average/', PupilAverageGradeView.as_view(), name="pupil-average-grades"),
    # These two are responsible for calculating the special courses points;
    path('student/<int:pk>/special-courses/', SpecialCourseGradesView.as_view()),
    path('student/<int:pk>/special-courses/<str:class_code>/', SpecialCourseGradesView.as_view()),
    # Calculates the total points;
    #path('student/<int:pk>/points-summary/', TotalPointsSummaryView.as_view(), name="special-points-summary"),
    path('student/<int:pk>/<str:course_code>/points-summary-per-course-code/', TotalPointsSummaryByCourseCodeView.as_view(), name="points-summary-per-course-code"),
    # Calculates the points summary with pupil name passed as the parameter;
    path('student/points-summary/<str:name>/', TotalPointsSummaryViewPerName.as_view(), name="special-points-summary-per-name"),
]
