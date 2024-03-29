from rest_framework import serializers
from patient.models import CustomUser, Document,Specialisation

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields=['email','password',]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','age','place','phone_number','email']

class SpecialisationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Specialisation
        fields='__all__'