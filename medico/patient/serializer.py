from rest_framework import serializers
from .models import CustomUser,TimeSlot,SlotBooking,Payment

class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'age', 'place', 'exp', 'specialisation', 'is_active', 'is_staff', 'date_joined', 'role', 'otp', 'password'] 
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password') 
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:CustomUser
    fields=['id','email','first_name','last_name','phone_number','place','age']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'place', 'age']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'phone_number','exp', 'specialisation', 'profile_image','consultation_fee']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model=TimeSlot
        fields='__all__'

class SlotBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotBooking
        fields = ['doctor', 'patient', 'date', 'start_time','timeslot', 'payment_completed']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['doctor','patient','consultation_date','amount']