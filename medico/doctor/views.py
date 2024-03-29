from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializer import *
from .docemail import *
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
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
        specialisation_id = data.get('specialisation')
        new_specialisation = data.get('new_specialisation')
        exp = data.get('exp')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        print(new_specialisation,".........newspecialization.................")
        # Check if passwords match
        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Handle new specialisation
        # if specialisation_id == 'other' and new_specialisation:
        #     specialisation_instance, created = Specialisation.objects.get_or_create(name=new_specialisation)
        # else:
        #     # Existing logic to get specialization by ID
        specialisation_instance = Specialisation.objects.get(id=specialisation_id)
        return Response({'error': 'Specialisation does not exist'}, status=status.HTTP_400_BAD_REQUEST)


        # Create CustomUser instance
        custom_user = CustomUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            exp=exp,
            role='doctor', # Set role to 'doctor'
            specialisation=specialisation_instance # Assign the Specialisation instance
        )

        # Set password
        custom_user.set_password(password)
        custom_user.save()

        # Create Document instance with uploaded files
        experience_certificate_file = request.FILES.get('experience_certificate')
        mbbs_certificate_file = request.FILES.get('mbbs_certificate')
        if experience_certificate_file and mbbs_certificate_file:
            Document.objects.create(
                user=custom_user,
                experience_certificate=experience_certificate_file,
                mbbs_certificate=mbbs_certificate_file
            )
        else:
            return Response({'error': 'Both experience certificate and MBBS certificate are required'}, status=status.HTTP_400_BAD_REQUEST)
        sent_otp_email(email)
        return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
    

    
class Verify_Otp(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email:
            return Response({'error': 'Email not found. Please Register Again'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not otp:
            return Response({'error': 'Please enter OTP!'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'email': email, 'otp': otp}
        serializer = VerifyUserSerializer(data=data)
        
        if serializer.is_valid():
            user = CustomUser.objects.get(email=email)
            send_mail_func_to_doc(serializer.data['email'])

            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.otp != otp:
                return Response({'error': 'Invalid OTP!'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_verified = True
            user.otp = None
            user.save()
           
            
            return Response({'status': 200, 'message': 'Account verified'})
        else:
            return Response({'status': 400, 'message': 'Validation error', 'error': serializer.errors})


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

