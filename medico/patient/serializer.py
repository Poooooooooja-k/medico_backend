from rest_framework import serializers
from .models import CustomUser, Document

class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False) 

    class Meta:
        model=CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'place', 'phone_number', 'age', 'exp', 'specialisation', 'is_active', 'is_staff', 'date_joined', 'role','otp','password']
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']

    def create(self, validated_data):
        password=validated_data.pop('password')
        instance=self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()