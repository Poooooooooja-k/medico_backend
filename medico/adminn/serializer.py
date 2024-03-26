from rest_framework import serializers
from .models import CustomUser, Document,specialisation

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields=['email','password',]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','age','place','phone_number','email']

class SpecialisationSerializer(serializers.ModelSerializer):
    class Meta:
        model=specialisation
        fields='__all__'