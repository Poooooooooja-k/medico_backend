from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import generics
from .docemail import *
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import QueryDict
import json

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

        # Check if passwords match
        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create CustomUser instance first
        custom_user = CustomUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            specialisation=specialisation,
            phone_number=phone_number,
            exp=exp,
            role='doctor', # Set role to 'doctor'
            is_approved=False 
        )

        # Set password
        custom_user.set_password(password)
        custom_user.save()

        # Now create the DocSpecialisation instance and associate it with the CustomUser instance
        specialisation_instance, created = DocSpecialisation.objects.get_or_create(
        name=specialisation,
        defaults={'is_active': True, 'user': custom_user} # Associate with the CustomUser instance
        )

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
        print(data,"--------------data-----------------")
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
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Incorrect email or password!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({'error': 'User account is inactive!'}, status=status.HTTP_401_UNAUTHORIZED)      
        
        if not user.is_approved:
            return Response({'error': 'Doctor account not approved yet. Please wait for approval.'}, status=status.HTTP_403_FORBIDDEN)
        
         # Generate JWT token
        refresh = RefreshToken.for_user(user)       
        return Response({'access_token': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)

class DoctorProfileAPIView(generics.RetrieveAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user # Access the authenticated user directly
        serializer = DoctorProfileSerializer(user)  # Serialize the user data
        return Response(serializer.data)
    
class UpdateProfileImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        print("--------------")
        profile_image=request.FILES.get('profile_image')
        print("------",request.data)
        serializer = UpdateProfileImageSerializer(request.user, data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("error",serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        return Response("GET request is allowed.")
        

class TimeSlotCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        data = request.data
        print("==",data)
        serializer = TimeSlotSerializer(data=data)
        doctor = request.user.id
        print('id',doctor)
        if serializer.is_valid():
            serializer.save(Doctor=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DocBlogAdd(APIView):
     def post(self,request):
        data=request.data
        print(data,"--------data---------")
        serializer=DocBlogSerializer(data=data)
        print(serializer,"------ser----------")
        if serializer.is_valid():
            print(serializer.is_valid(),"-------isvalios---------------")
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     
class DocViewPost(APIView):
      def get(self, request):
        blogs = BlogPost.objects.filter(is_verified=True)
        serializer = DocBlogSerializer(blogs, many=True)
        return Response(serializer.data)
      
class AddConsultationFee(APIView):
    def post(self,request):
        serializer = ConsultationFeeSerializer(request.user, data=request.data)
        print(request.user,"--------userooooooooooo")
        print(serializer,"----ser------------")
        if serializer.is_valid():
            print(serializer.is_valid(),"--------valid----------")
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class DoctorDocumentsget(APIView):
    def get(self, request):
        try:
            doctor = request.user
            print(doctor,"-------------------")
            documents = Document.objects.filter(user=doctor)
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetTimeSlotsView(APIView):
    def get(self, request, date):
        try:
            slots = TimeSlot.objects.filter(date=date, available=True)
            times = [slot.start_time for slot in slots]
            
            # serializer=TimeSlotSerializer(data=slots,many=True)
            # if serializer.is_valid():
            return Response(times, status=status.HTTP_200_OK)
        except TimeSlot.DoesNotExist:
            return Response({'error': 'No time slots found for the given date.'}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteSlot(APIView):
    def post(self,request):
        slot_id=request.data.get('slot_id')
        print(slot_id,"-----------slotid--------------")
        try:
            slot=TimeSlot.objects.get(id=slot_id)
            slot.delete()
            return Response({'message':'slot deleted successfully!!'},status=status.HTTP_200_OK)
        except TimeSlot.DoesNotExist:
            return Response({'error':'time slot not found'},status=status.HTTP_400_BAD_REQUEST)
            
class DocblogDelete(APIView):
    def get(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk,is_active=True)
            blog.is_active=False
            blog.save()
            return Response({'message':'Blog deactivated successfully!!'},status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'error':'blog not found or already activated'},status=status.HTTP_400_BAD_REQUEST)
        

class DocblogRestore(APIView):
    def get(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk,is_active=False)
            blog.is_active=True
            blog.save()
            return Response({'message':'blog restored successfully'},status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'error':'error restoring blog'},status=status.HTTP_400_BAD_REQUEST)
        

class DocBlogEdit(APIView):
    def get(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk)
            serializer=DocBlogEditSerializer(blog)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
    def patch(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk)
            serializer = DocBlogEditSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
