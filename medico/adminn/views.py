
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import specialisation
from .models import CustomUser
from patient.serializer import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

from rest_framework.viewsets import ModelViewSet



class AdminLogin(APIView):
    def post(self,request):
        data=request.data
        email=data.get('email')
        password=data.get('password')
        print(email)
        print(password)
        if not(email and password):
            return AuthenticationFailed({
                'error':'Email and password required'
            })
        user=CustomUser.objects.filter(email=email,is_staff=True).first()
        
        if user is None:
            raise AuthenticationFailed({
                'error':'Admin access is required'
            })
        if not user.check_password(password):
            raise AuthenticationFailed({'error':'incorrect password!!'})
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)

class DoctorListView(APIView):
    def get(self, request):
        doctors = CustomUser.objects.filter(role='doctor')
        serializer = CustomUserSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApproveDoctorView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        email = request.data.get('email')
        doctor = CustomUser.objects.filter(email=email, role='doctor').first()
        if not doctor:
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

        if doctor.is_approved:
            return Response({'error': 'Doctor account is already approved.'}, status=status.HTTP_400_BAD_REQUEST)
        doctor.is_approved = True
        doctor.save()
        return Response({'message': 'Doctor account approved successfully.'}, status=status.HTTP_200_OK)

class PatientListView(APIView):
    def get(self, request):
        patients = CustomUser.objects.filter(role='patient', is_staff=False)
        serializer = CustomUserSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PatientUpdate(APIView):
    def post(self,request,pk):
        try:
            patient=CustomUser.objects.get(pk=pk)
        except CustomUser.DoesnotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=PatientSerializer(patient,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PatientDelete(APIView):
    def get(self,request,pk):
        try:
            patient=CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error':'Patient not found'},status=status.HTTP_400_BAD_REQUEST)
        patient.delete()
        return Response({'error':'patient deleted successfully!!'})

class AddSpecialisation(APIView):
    def post(self, request):
        print(request.data," dffffffffffffffffffffffffff")
        serializer = SpecialisationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SpecialisationListView(ListAPIView):
#     queryset = specialisation.objects.all()
#     serializer_class = SpecialisationSerializer
    
class SpecialisationViewSet(ModelViewSet):
    queryset = specialisation.objects.all()
    serializer_class = SpecialisationSerializer

# class SpecialisationListDetail(RetrieveAPIView):
#     queryset = specialisation.objects.all()
#     serializer_class = SpecialisationSerializer