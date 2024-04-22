from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework import generics
from .email import *
from rest_framework import permissions,status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import logout
import razorpay
client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY_ID, settings.KEY_SECRET))

class PatientSign(APIView):
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
            send_mail_func(serializer.data['email'])

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


class PatientLogin(APIView):
    def post(self,request):
        data=request.data
        email=data.get('email')
        password=data.get('password')
        
        if not(email and password):
            return Response({'error':'Email and password is required!!'})
        
        user=CustomUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed({'error':'User is not Found!!'})
        if not user.check_password(password):
            raise AuthenticationFailed({'error':'Incorrect password!!'})

        refresh = RefreshToken.for_user(user)  
        return Response({'access_token': str(refresh.access_token), 'refresh': str(refresh)}, status=status.HTTP_200_OK)


class PatientProfile(generics.RetrieveAPIView):
    serializer=ProfileSerializer()
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        serializer=ProfileSerializer(user)
        return Response(serializer.data)
    
    
class DoctorList(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='doctor', is_approved=True)  # Filter doctors who are approved
    serializer_class = DoctorSerializer

class DoctorDetails(APIView):
    def post(self,request):
        doctor_id=request.data['doctor_id']
        print(doctor_id,"-----------")
        try:
            doctor=CustomUser.objects.get(id=doctor_id,role='doctor')
            serializer=DoctorSerializer(doctor)
            return Response(serializer.data)
        except:
            return Response({'error':'doctor not found'},status=status.HTTP_400_BAD_REQUEST)

class DocgetSlot(APIView):
    def post(self, request):
        data=request.data
        print(data,"----------data---------------")
        selected_date = request.data['selected_date']
        doctor_id = request.data['doctor_id']

        time_slots = TimeSlot.objects.filter(Doctor_id=doctor_id, date=selected_date, available=True)
        serializer = TimeSlotSerializer(time_slots, many=True)
        return Response({'time_slots': serializer.data}, status=status.HTTP_200_OK)

class BookSlotAPIView(APIView):
    def post(self, request, format=None):
        patient=request.user
        print(patient,"-------------")
        user=CustomUser.objects.get(email=patient,role='patient')
        patient_id=user.id 
        print(patient_id,"-------id-------------")
        data=request.data
        data['patient']=str(patient_id)
        print(data,'-----------data-------------')
        serializer = SlotBookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class patientPayment(APIView):
    def post(self,request):
        doctor_id = request.data.get('doctor_id')
        amount = request.data.get('amount')
        consultation_date = request.data.get('consultation_date')
         # Create booking with Razorpay
        booking_data = {
            'amount': amount * 100,  # Razorpay expects amount in paisa
            'currency': 'INR',
            'receipt': 'receipt_order_{}'.format(doctor_id),
            'payment_capture': 1  # Auto-capture payment
        }
        order = client.order.create(data=booking_data)
        user=request.user
        user=CustomUser.objects.get(email=user)
        user_id=user.id
        data = {
            'patient':user_id,  # Assuming user is authenticated and is a patient
            'doctor': doctor_id,
            'amount': amount,
            'consultation_date': consultation_date,
            'razorpay_order_id': order['id']  # Save Razorpay order ID for future reference
        }
        # serializer = PaymentSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(data,status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class handlePaymentSuccess(APIView):
    def post(self,request):
        razorpay_payment_id = request.data['razorpay_payment_id']
        razorpay_order_id = request.data['razorpay_order_id']
        razorpay_signature = request.data['razorpay_signature']
        doctor=request.data['doctor']
        patient=request.data['patient']
        date=request.data['consultation_date']
        amount=request.data['amount']

        data={
            ' razorpay_payment_id ': razorpay_payment_id ,
            ' razorpay_order_id': razorpay_order_id,
            ' razorpay_signature ': razorpay_signature ,
        }
        check=client.utility.verify_payment_signature(data)
        if check is None:
            return Response({'error':'Error while payment'},status=status.HTTP_400_BAD_REQUEST)
        details={
            'doctor':doctor,
            'patient':patient,
            'consultation_date':date,
            'amount':amount
        }
        serializer=PaymentSerializer(data=details)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,{'message':'payment success'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




