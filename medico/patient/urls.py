from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
#    path('patientsignup/',PatientSignup.as_view()),
   path('verifyotp/',Verify_Otp.as_view()),
   path('signup/',Sign.as_view()),
]
