from student.serializers import (
                                  PupilSerializer,
                                  PupilCoursesSerializer
                                )
from student.models import (
                             Pupil,
                             PupilClassesCoursesGrades
                           )
from rest_framework.generics import  (
                                      ListCreateAPIView,
                                      ListAPIView,
                                      CreateAPIView,
                                      RetrieveUpdateDestroyAPIView
                                     )
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework  import status

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