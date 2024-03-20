from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializer import *
from patient.models import *
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser

class DocSignupView(APIView):
    parser_classes = (MultiPartParser, FormParser) 
    def post(self, request):
        data = request.data
        # Extract data from request
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        specialisation = data.get('specialisation')
        exp = data.get('exp')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        print(first_name)
        print(last_name)
        print(email)
        # Check if passwords match
        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create CustomUser instance
        custom_user = CustomUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            specialisation=specialisation,
            exp=exp,
            role='doctor'  # Set role to 'doctor'
        )
        # Set password
        custom_user.set_password(password)
        custom_user.save()

        # Create Document instance with uploaded files
        experience_certificate_file = request.FILES.get('experience_certificate')
        mbbs_certificate_file = request.FILES.get('mbbs_certificate')
        if experience_certificate_file and mbbs_certificate_file:
            document = Document.objects.create(
                user=custom_user,
                experience_certificate=experience_certificate_file,
                mbbs_certificate=mbbs_certificate_file
            )
        else:
            # Handle case where one or both files are missing
            return Response({'error': 'Both experience certificate and MBBS certificate are required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class DocLogin(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        if not(email and password):
            return Response({
                'error':'Email and password is required!!'
            })
        user=CustomUser.objects.filter(email=email)
        if user is None or not user.check_password(password):
            raise AuthenticationFailed({'error': 'Incorrect email or password!'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            raise AuthenticationFailed({'error': 'User account is inactive!'}, status=status.HTTP_401_UNAUTHORIZED)
            
        if not user.is_approved:
            return Response({'error': 'Doctor account not approved yet.'}, status=status.HTTP_403_FORBIDDEN)

         # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)

