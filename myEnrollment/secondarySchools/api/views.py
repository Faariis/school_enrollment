
from secondarySchools.serializers import(
                                          CantonSerializer,
                                          SecondarySchoolSerializer,
                                          CoursesSecondarySchoolSerializer
                                        )
from teachersAuth.models import (
                                  Teacher,
                                )
from secondarySchools.models import (
                                      Canton,
                                      SecondarySchool,
                                      CoursesSecondarySchool
                                    )


from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import  (
                                      ListCreateAPIView,
                                      ListAPIView,
                                      CreateAPIView,
                                      RetrieveUpdateDestroyAPIView
                                     )
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework_simplejwt.views import TokenObtainPairView

import myEnrollment.settings as api_settings
from django.core.exceptions import ObjectDoesNotExist

class SchoolView(ListCreateAPIView):
    # queryset = SecondarySchool.objects.all() # we use custom manager
    serializer_class = SecondarySchoolSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SecondarySchool.objects.all()

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        teacher= Teacher.objects.get(id= request.auth['user_id'])
        # teacher= Teacher.objects.get(id= 1)
        schools= Teacher.objects.values_list('school_id', flat=True).filter(id=teacher.id)
        school_id_queryset= SecondarySchool.objects.get(id= schools[0])
        serializer= SecondarySchoolSerializer(school_id_queryset)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        # Only superuser can create new school
        is_superuser= Teacher.objects.get(id= request.auth['user_id']).is_superuser
        # is_superuser=1 
        if is_superuser:
            serializer= SecondarySchoolSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status.HTTP_403_FORBIDDEN)

class SchoolViewDetail(RetrieveUpdateDestroyAPIView):
    queryset= SecondarySchool.objects.all()
    serializer_class= SecondarySchoolSerializer
    # Only superuser can update school
    permission_classes= [IsAdminUser]

# On single object
class SchoolCoursesCreateView(CreateAPIView):
    serializer_class= CoursesSecondarySchoolSerializer
    permission_classes= [IsAdminUser]
    def perform_create(self, serializer):
        pk= self.kwargs['pk']
        school= SecondarySchool.objects.get(id= pk)
        serializer.save(school_id= school)

class SchoolCoursesListView(ListAPIView):
    serializer_class= CoursesSecondarySchoolSerializer
    permission_classes= [IsAuthenticated]
    def get_queryset(self):
        pk= self.kwargs['pk']
        return CoursesSecondarySchool.objects.filter(school_id=pk)

class CantonView(ListAPIView):
    permission_classes= [IsAuthenticated]
    queryset= Canton.objects.all()
    serializer_class= CantonSerializer
    paginate_by= 5

    def get_queryset(self):
        return  Canton.objects.order_by('_canton_code')

class CantonDetailView(RetrieveUpdateDestroyAPIView):
    lookup_field="_canton_code"
    serializer_class= CantonSerializer
    permission_classes= [IsAdminUser]

    def get_queryset(self):
        return Canton.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            instance = Canton.objects.get(_canton_code= self.kwargs['_canton_code'])
        except ObjectDoesNotExist:
            instance= Canton(_canton_code= self.kwargs['_canton_code'])
            # ^ using above to mimic create/post,although it shouldn't be allowed
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = CantonSerializer(instance, data=request.data,
                                      partial= False)
        if serializer.is_valid():
            serializer.save()
            return Response(status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CantonSchoolView(ListCreateAPIView):
    serializer_class= SecondarySchoolSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        school_canton_code= self.kwargs['canton_code']
        obj= SecondarySchool.objects.filter(school_canton_code=school_canton_code)
        return obj

    def list(self, request, *args, **kwargs):
        queryset= self.get_queryset()
        serializer= SecondarySchoolSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        school_canton_code= self.kwargs['canton_code']
        school_canton_code_obj= Canton(_canton_code= school_canton_code)
        serializer= SecondarySchoolSerializer(data=request.data)
        if  serializer.is_valid():
            serializer.save(school_canton_code= school_canton_code_obj)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CantonSchoolDetailView(RetrieveUpdateDestroyAPIView):
    queryset= SecondarySchool.objects.all()
    serializer_class= SecondarySchoolSerializer
    permission_classes= [IsAdminUser]
    
