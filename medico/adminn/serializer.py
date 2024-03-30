from rest_framework import serializers
from patient.models import CustomUser, Document,DocSpecialisation


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields=['email','password',]

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','age','place','phone_number','email']



class DocSpecialisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocSpecialisation
        fields = ['name']


class DocDocumentSerializer(serializers.ModelSerializer):
    experience_certificate = serializers.ImageField(max_length=None, use_url=True)
    mbbs_certificate = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Document
        fields = ['experience_certificate', 'mbbs_certificate']

class DoctorSerializer(serializers.ModelSerializer):
    doc_image = DocDocumentSerializer(many=True, read_only=True, source='document_set')
    specialisation = DocSpecialisationSerializer(source='docspecialisation_set', many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'exp', 'role', 'is_approved', 'specialisation', 'doc_image']



class SpecialisationSerializer(serializers.ModelSerializer):
    class Meta:
        model=DocSpecialisation
        fields='__all__'