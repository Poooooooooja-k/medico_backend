from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'specialisations', SpecialisationViewSet)


urlpatterns = [
   path('adminlogin/',AdminLogin.as_view()),
   path('doctorverify/',ApproveDoctorView.as_view()),
   path('rejectdoctor/',RejectDoctor.as_view()),
   path('doctorlist/',DoctorListView.as_view()),
   path('patientlist/',PatientListView.as_view()),
   path('patientupdate/<int:pk>/', PatientUpdate.as_view()),
   path('patientdelete/<int:pk>/',PatientDelete.as_view(), name='patient-delete'),
   path('patientrestore/<int:pk>/',PatientRestore.as_view(), name='patient-restore'),
   path('specrestore/<int:pk>/', SpecialisationRestore.as_view()),
   path('specdelete/<int:pk>/', SpecialisationDelete.as_view()),
   path('addspecialisation/',AddSpecialisation.as_view()),
   path('doctorlist/',DoctorListView.as_view()),
   path('addblog/',AddPost.as_view()),
   path('adminviewpost/',ViewPost.as_view()),
   path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
