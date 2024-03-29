from rest_framework import serializers
from .models import CustomUser, Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['experience_certificate', 'mbbs_certificate']

class CustomUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(required=False) 
    password = serializers.CharField(write_only=True)  # For password field
    confirm_password = serializers.CharField(write_only=True)  # For confirm_password field
    document = DocumentSerializer(required=True)

    class Meta:
        model=CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'place', 'phone_number', 'age', 'exp', 'specialisation', 'is_active', 'is_staff', 'date_joined', 'role','password','document','confirm_password']
        read_only_fields = ['id', 'is_active', 'is_staff', 'date_joined']


    def create(self, validated_data):
        # Extract document data
        document_data = validated_data.pop('document')
        # Extract password data
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        # Create the user
        user = CustomUser.objects.create(**validated_data)
        # Set password
        user.set_password(password)
        user.save()

        # Create the associated document
        Document.objects.create(user=user, **document_data)

        return user
