from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
#    path('patientsignup/',PatientSignup.as_view()),
    path('verifyotp/',Verify_Otp.as_view()),
    path('patientsignup/',PatientSign.as_view()),
    path('patientlogin/',PatientLogin.as_view()),
    path('userprofile/',PatientProfile.as_view()),
    path('listdoctors/', DoctorList.as_view()),
]
