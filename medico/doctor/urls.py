from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path('docsignup/',DocSignupView.as_view()),
   path('verifyotp/', Verify_Otp.as_view()),
   path('doclogin/',DocLogin.as_view()),
   
]
