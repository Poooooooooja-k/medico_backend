from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path('docsignup/',DocSignupView.as_view()),
   path('verifyotp/', Verify_Otp.as_view()),
   path('doclogin/',DocLogin.as_view()),
   path('docprofile/', DoctorProfileAPIView.as_view()),
   path('profileimage/',UpdateProfileImageView.as_view()),
   path('createtimeslot/',TimeSlotCreate.as_view()),
   path('docaddblog/',DocBlogAdd.as_view()),
   path('docviewpost/',DocViewPost.as_view()),
   path('docblogdelete/',DocblogDelete.as_view()),
   path('docblogrestore/',DocblogRestore.as_view()),
   path('doceditblog/<int:pk>/', DocBlogEdit.as_view()),
   path('addfee/',AddConsultationFee.as_view()),
   path('getdocdocuments/',DoctorDocumentsget.as_view()),
   path('gettimeslots/<str:date>/', GetTimeSlotsView.as_view(), name='get_time_slots'),
   path('deleteslot/',DeleteSlot.as_view()),
]  
