from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'specialisations', SpecialisationViewSet)

urlpatterns = [
   path('adminlogin/',AdminLogin.as_view()),
   path('doctorverify/',ApproveDoctorView.as_view()),
   path('doctorlist/',DoctorListView.as_view()),
   path('patientlist/',PatientListView.as_view()),
   path('patientupdate/<int:pk>/', PatientUpdate.as_view()),
   path('patientdelete/<int:pk>/',PatientDelete.as_view()),
   path('addspecialisation/',AddSpecialisation.as_view()),
   # path('viewspecialisation/',SpecialisationListView.as_view()),
   # path('viewspecialisation/<int:pk>/',SpecialisationListDetail.as_view()),
   path('', include(router.urls)),
]
