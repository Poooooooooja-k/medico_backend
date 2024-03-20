from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
   path('doctorverify/',ApproveDoctorView.as_view()),
   path('doctorlist/',DoctorListView.as_view()),
]
