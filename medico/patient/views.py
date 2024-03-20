from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from .serializer import *
from .models import *
from .email import *
from rest_framework import permissions,status


# Create your views here.
# class PatientSignup(APIView):
#     def post(self,request):
#         print(request.data)
#         first_name=request.data.get('first_name')
#         last_name=request.data.get('last_name')
#         age=request.data.get('age')
#         place=request.data.get('place')
#         phone_number=request.data.get('phone_number')
#         email=request.data.get('email')
#         password = request.data.get('password')
#         confirm_password = request.data.get('confirm_password')

#         if password!=confirm_password:
#             return Response({'error':'password doesnot match!!'},status.HTTP_400_BAD_REQUEST)
        
#           # Check if email already exists
#         # if CustomUser.objects.filter(email=email).exists():
#         #     return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
#         if CustomUser.objects.filter(email__iexact=email).exists():
#             raise ValidationError({'email': ['A user with this email already exists.']})


#         # custom_user=CustomUser.objects.create(
#         #     first_name=first_name,
#         #     last_name=last_name,
#         #     age=age,
#         #     place=place,
#         #     phone_number=phone_number,
#         #     email=email,
#         #     role='patient'
#         # )
#         #  Set password
        
#         # custom_user.set_password(password)
#         # custom_user.save()

#         serializer = CustomUserSerializer(data = request.data)
#         if serializer.is_valid():
#             print(serializer,"just testing")
#             serializer.save()
#             sent_otp_email(serializer.data['email'])
#             return Response({'message': 'Registration successful. Please check your email for OTP verification.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors) 
#         # return Response({'message': 'Registration successful. Please check your email for OTP verification.', 'data': serializer.data}, status=status.HTTP_201_CREATED)

class Sign(APIView):
    def post(self,request):
        data =request.data
        email=data.get('email')
        password=data.get('password')
        confirm_password=data.get('confirm_password')

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError({'email': ['A user with this email already exists.']})
        
        if password!=confirm_password:
            return Response({'error':'password doesnot match'},status=status.HTTP_400_BAD_REQUEST)
        
        serializer=CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            sent_otp_email(serializer.data['email'])
            return Response({'message': 'Registration successful. Please check your email for OTP verification.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
       
class Verify_Otp(APIView):
        def post(self,request):
            email=request.data.get('email')
            otp=request.data.get('otp')
            if not email:
               return Response({'error':'Email not found Please Register Again'},status=status.HTTP_400_BAD_REQUEST)
            
            if not otp:
                return Response({'error':'Please enter otp!'},status=status.HTTP_400_BAD_REQUEST)
            data=request.data
            serializer=VerifyUserSerializer(data=data)
            if serializer.is_valid:
                user=CustomUser.objects.get(email=email)
                print("OTP",user.otp)
                if not user:
                    return Response({'error':'User not found'},status=status.HTTP_400_BAD_REQUEST)
                if user.otp!=otp:
                    return Response({'error':'Invalid otp!'},status=status.HTTP_400_BAD_REQUEST)
                user.is_verified=True
                user.otp=None
                user.save()
                send_mail_func.delay()
                return Response({'status':200,'message':'Account verified'})
            return Response({'status':400,'message':'validation error','error':'serializer.errors'})

    # class ResentOtp(APIView):
    #     def post(self,request,*args,**kwargs):
    #         email=request.data.get('email')
    #         if email:
    #             user=CustomUser.objects.filter(email_iexact=email)

