from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from .serializer import *
from .models import *
from rest_framework import permissions,status

# Create your views here.
class PatientSignup(APIView):
    def post(self,request):
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        age=request.data.get('age')
        place=request.data.get('place')
        phone_number=request.data.get('phone_number')
        email=request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password!=confirm_password:
            return Response({'error':'password doesnot match!!'},status.HTTP_400_BAD_REQUEST)
        
          # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        
        custom_user=CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            place=place,
            phone_number=phone_number,
            email=email,
            role='patient'
        )
         # Set password
        custom_user.set_password(password)
        custom_user.save()

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
