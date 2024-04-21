from django.db.models import Avg
from django.http import JsonResponse
from student.serializers import (
                                  PupilSerializer,
                                  PupilCoursesSerializer,
                                  PupilAcknowledgmentsSerializer
                                )
from student.models import (
                             Pupil,
                             PupilClassesCoursesGrades,
                             Courses,
                             PupilClassesAcknowledgments,
                             SpecialCoursesPerDesiredChoice
                           )
from rest_framework.generics import  (
                                      ListCreateAPIView,
                                      ListAPIView,
                                      CreateAPIView,
                                      RetrieveUpdateDestroyAPIView,
                                      RetrieveUpdateAPIView
                                     )
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework  import status
from rest_framework.exceptions import NotFound

class ApiOverview(APIView):
    def get(self, request):
        api_urls = {
         }
        return Response(api_urls)


class PupilView(ListCreateAPIView):
    # queryset = SecondarySchool.objects.all() # we use custom manager
    serializer_class = PupilSerializer
    permission_classes = [AllowAny]
    queryset= Pupil.objects.all()
    def get_queryset(self):
        return Pupil.objects.all()
    
    def list(self, request):
        #import pdb
        #pdb.set_trace()
        qs= self.get_queryset()
        serializer= self.serializer_class(qs, many= True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer= PupilSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
        else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PupilViewDetail(RetrieveUpdateDestroyAPIView):
    queryset= Pupil.objects.all()
    serializer_class= PupilSerializer
    # Only superuser can update school
    permission_classes= [AllowAny]


class PupilCoursesView(ListCreateAPIView):
    # queryset = SecondarySchool.objects.all() # we use custom manager
    serializer_class = PupilCoursesSerializer
    permission_classes = [AllowAny]
    queryset= Pupil.objects.all()

    # Make sure that normal users can get only current form to update
    def get(self, request, *args, **kwargs):
        pk= self.kwargs['pk']
        # import pdb
        # pdb.set_trace()
        pupil_id1= Pupil.objects.filter(id= pk).first()
        pupil_courses= PupilClassesCoursesGrades.objects.filter(pupil_id=pupil_id1)
        serializer= self.serializer_class(pupil_courses, many= True)
        return Response(serializer.data)



class PupilCoursesDetailView(RetrieveUpdateDestroyAPIView):
    queryset= PupilClassesCoursesGrades.objects.all()
    serializer_class= PupilCoursesSerializer
    # Only superuser can update school
    permission_classes= [AllowAny]


# On single object /student/pk <post>
class PupilCreateView(CreateAPIView):
    serializer_class= PupilSerializer
    permission_classes= [IsAdminUser]
    def perform_create(self, serializer):
        pk= self.kwargs['pk']
        school= Pupil.objects.get(id= pk)
        serializer.save(school_id= school)


class PupilClassCourseView(APIView):
    permission_classes= [AllowAny]

    def get(self, request):
        GRADE_CHOICES= ['VI', 'VII', 'VIII', 'IX']
        response= []

        for grade in GRADE_CHOICES:
            class_courses = Courses.objects.filter(**{'class_' + grade: True})

            response.extend([{
                'class_id': grade,
                'course_code': course.course_code,
                'course_name': course.course_name
            } for course in class_courses])

        return Response(response, status=200)


# New view for calculating acknowledgment points;
from .helpers import calculate_ack_points
class PupilClassAcknowledgmentView(APIView):
    serializer_class = PupilAcknowledgmentsSerializer
    permission_classes = [AllowAny]
    queryset = Pupil.objects.all()

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            pupil = Pupil.objects.get(pk=pk)
        except Pupil.DoesNotExist:
            raise NotFound("Pupil does not exist", code=status.HTTP_404_NOT_FOUND)
        pupil_acknowledgments = PupilClassesAcknowledgments.objects.filter(pupil_id=pk)
        """ many= True means that the serializer expects a list of object and every 
        object needs to be serialized"""
        serializer = self.serializer_class(pupil_acknowledgments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ack_position = serializer.validated_data['ack_position']
            ack_level = serializer.validated_data['ack_level']
            ack_points = calculate_ack_points(ack_position, ack_level)

            serializer.validated_data['ack_points'] = ack_points
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# New view that returns average grades;
class PupilAverageGradeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            pupil = Pupil.objects.get(pk=pk)
        except Pupil.DoesNotExist:
            return Response({"error": "Pupil not found."}, status=status.HTTP_404_NOT_FOUND)

        class_ids = ['VI', 'VII', 'VIII', 'IX']
        response_data = {}
        points_grades = 0

        for class_id in class_ids:
            grades = PupilClassesCoursesGrades.objects.filter(pupil_id=pupil, class_id=class_id)
            average_score = grades.aggregate(avg_score=Avg("score"))['avg_score']
            average_score = round(average_score, 2) if average_score else None
            points_grades += average_score or 0
            response_data[f'average_{class_id}'] = average_score

        points_grades *= 3
        response_data['points'] = round(points_grades, 2)
        student_course = pupil.desired_course_A
        print(student_course)

        return Response(response_data, status=status.HTTP_200_OK)


class SpecialCourseGradesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, class_code=None):
        try:
            pupil = Pupil.objects.get(pk=pk)
        except Pupil.DoesNotExist:
            return Response({"error": "Pupil not found."}, status=status.HTTP_404_NOT_FOUND)

        # Filter special courses based on class code if provided
        special_courses = SpecialCoursesPerDesiredChoice.objects.filter(
            school_id=pupil.secondary_shool_id,
            primary_class_code__in=['VIII', 'IX'],
        )
        if class_code:
            special_courses = special_courses.filter(course_code=class_code)

        response_data = {}

        for special_course in special_courses:
            # Get the grades for the special course
            grades = PupilClassesCoursesGrades.objects.filter(
                pupil_id=pupil,
                class_id=special_course.primary_class_code,
                course_code=special_course.primary_class_course_code_id,
            )

            average_score = grades.aggregate(avg_score=Avg("score"))['avg_score']
            average_score = round(average_score, 2) if average_score else None

            if special_course.course_code_id in response_data:
                response_data[special_course.course_code_id][f"{special_course.primary_class_code_id}_{special_course.primary_class_course_code_id}"] = average_score
            else:
                response_data[special_course.course_code_id] = {"course": special_course.course_code_id}
                response_data[special_course.course_code_id][f"{special_course.primary_class_code_id}_{special_course.primary_class_course_code_id}"] = average_score

        # Total points
        for course_data in response_data.values():
            total_points = sum(score for score in course_data.values() if isinstance(score, (int, float)))
            course_data['total_special_points'] = total_points

        response_list = list(response_data.values())

        return Response(response_list, status=status.HTTP_200_OK)


# New view that sums acknowledgment points; 
class TotalAcknowledgmentPointsView(APIView):
    serializer_class = PupilAcknowledgmentsSerializer
    permission_classes = [AllowAny]
    queryset = Pupil.objects.all()

    def get(self, request, pk):
        try:
            pupil = Pupil.objects.get(pk=pk)
        except Pupil.DoesNotExist:
            return Response({"error": "Pupil not found."}, status=status.HTTP_404_NOT_FOUND)

        pupil_acknowledgments = PupilClassesAcknowledgments.objects.filter(pupil_id=pupil)

        # Federal, canton, district, total_ack_points;
        total_federal_points = sum([ack.ack_points for ack in pupil_acknowledgments if ack.ack_level == "Federalno"])
        total_canton_points = sum([ack.ack_points for ack in pupil_acknowledgments if ack.ack_level == "Kantonalno"])
        total_district_points = sum([ack.ack_points for ack in pupil_acknowledgments if ack.ack_level == "Općinsko"])
        total_ack_points = total_federal_points + total_canton_points + total_district_points

        response_data = {
            "total_federal_points": total_federal_points,
            "total_canton_points": total_canton_points,
            "total_district_points": total_district_points,
            "total_ack_points": total_ack_points
        }
        return Response(response_data, status=status.HTTP_200_OK)


# New view that sums all points for one student but for all courses;
"""class TotalPointsSummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            pupil = Pupil.objects.get(pk=pk)
        except Pupil.DoesNotExist:
            return Response({"error": "Pupil not found."}, status=status.HTTP_404_NOT_FOUND)

        # We need to get the points from PupilAverageGradeView;
        average_grade_response = PupilAverageGradeView().get(request, pk).data
        points = average_grade_response.get("points", 0)

        # We need to get the points from TotalAcknowledgmentPointsView;
        acknowledgment_response = TotalAcknowledgmentPointsView().get(request, pk).data
        total_ack_points = acknowledgment_response.get("total_ack_points", 0)

        # We need to get the points from AllSpecialCourseGradesView;
        special_grades_response = SpecialCourseGradesView().get(request, pk).data

        summary_data = []

        # From every object of AllSpecialCourseGradesView we get the points and course;
        for special_grade in special_grades_response:
            course = special_grade.get("course")
            total_special_points = special_grade.get("total_special_points")

            # Total points
            total_points = round(points + total_ack_points + total_special_points, 2)

            summary_data.append({
                "course": course,
                "total_points": total_points
            })

        return Response(summary_data, status=status.HTTP_200_OK)"""


# Here we get the total points but per course code;
class TotalPointsSummaryByCourseCodeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk, course_code):
        try:
            pupil = Pupil.objects.get(pk=pk)
        except Pupil.DoesNotExist:
            return Response({"error": "Pupil not found."}, status=status.HTTP_404_NOT_FOUND)

        # We need to get the points from PupilAverageGradeView;
        average_grade_response = PupilAverageGradeView().get(request, pk).data
        points = average_grade_response.get("points", 0)

        # We need to get the points from TotalAcknowledgmentPointsView;
        acknowledgment_response = TotalAcknowledgmentPointsView().get(request, pk).data
        total_ack_points = acknowledgment_response.get("total_ack_points", 0)

        # We need to get the points from AllSpecialCourseGradesView;
        special_grades_response = SpecialCourseGradesView().get(request, pk).data
        special_grade = next((item for item in special_grades_response if item["course"] == course_code), None)

        if special_grade:
            # We get the points and course;
            course = special_grade.get("course")
            total_special_points = special_grade.get("total_special_points")

            # Total points;
            total_points = round(points + total_ack_points + total_special_points, 2)

            return Response({
                "course": course,
                "total_points": total_points
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"No data found for course code: {course_code}"}, status=status.HTTP_404_NOT_FOUND)


# Total points per name adi;
class TotalPointsSummaryViewPerName(APIView):
    permission_classes = [AllowAny]

    def get(self, request, name):
        # Check if the name contains a space indicating separate first name and last name
        if " " in name:
            first_name, last_name = name.split(" ")
        else:
            # If the name does not contain a space, assume it's provided together
            # Splitting the name into first name and last name
            first_name = name[:-3]  # Assuming last 3 characters are the last name
            last_name = name[-3:]   # Assuming last 3 characters are the last name

        # Filter pupils by first and last name
        pupils = Pupil.objects.filter(name=first_name, last_name=last_name)

        if not pupils.exists():
            return Response({"error": "Pupil not found."}, status=status.HTTP_404_NOT_FOUND)

        pupil = pupils.first()  # Get the first pupil found

        # Assuming pk is obtained from the pupil object or somewhere else in the code
        pk = pupil.pk

        # We need to get the points from PupilAverageGradeView;
        average_grade_response = PupilAverageGradeView().get(request, pk).data
        points = average_grade_response.get("points", 0)

        # We need to get the points from TotalAcknowledgmentPointsView;
        acknowledgment_response = TotalAcknowledgmentPointsView().get(request, pk).data
        total_ack_points = acknowledgment_response.get("total_ack_points", 0)

        # We need to get the points from AllSpecialCourseGradesView;
        special_grades_response = SpecialCourseGradesView().get(request, pk).data

        summary_data = []

        # From every object of AllSpecialCourseGradesView we get the points and course;
        for special_grade in special_grades_response:
            course = special_grade.get("course")
            total_special_points = special_grade.get("total_special_points")

            # Total points
            total_points = round(points + total_ack_points + total_special_points, 2)

            summary_data.append({
                "id": pk,  # Adding ID of the pupil
                "course": course,
                "total_points": total_points
            })

        return Response(summary_data, status=status.HTTP_200_OK)


