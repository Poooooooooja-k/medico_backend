
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import CustomUser
from patient.serializer import *


class DoctorListView(APIView):
    permission_classes = [IsAdminUser]
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
