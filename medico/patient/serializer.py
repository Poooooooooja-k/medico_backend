from rest_framework import serializers
from .models import CustomUser, Document

class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False) 

    class Meta:
        model=CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'place', 'phone_number', 'age', 'exp', 'specialisation', 'is_active', 'is_staff', 'date_joined', 'role']
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']

