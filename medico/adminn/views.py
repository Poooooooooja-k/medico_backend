
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from patient.models import CustomUser,DocSpecialisation,BlogPost
from patient.serializer import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class AdminLogin(APIView):
    def post(self,request):
        data=request.data
        email=data.get('email')
        password=data.get('password')
        print(email)
        print(password)
        if not(email and password):
            return AuthenticationFailed({
                'error':'Email and password required'
            })
        user=CustomUser.objects.filter(email=email,is_staff=True).first()
        
        if user is None:
            raise AuthenticationFailed({
                'error':'Admin access is required'
            })
        if not user.check_password(password):
            raise AuthenticationFailed({'error':'incorrect password!!'})
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return Response({'access_token': access_token}, status=status.HTTP_200_OK)

class DoctorListView(APIView):
    def get(self, request):
        doctors = CustomUser.objects.filter(role='doctor')
        serializer = CustomUserSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApproveDoctorView(APIView):
    def post(self, request):
        email = request.data.get('email')

        # Filter doctor by email
        doctor = CustomUser.objects.filter(email=email, role='doctor').first()
        if not doctor:
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

        if doctor.is_approved:
            return Response({'error': 'Doctor account is already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        # Approve doctor
        doctor.is_approved = True
        doctor.save()
       
        return Response({'message': 'Doctor account approved successfully'}, status=status.HTTP_200_OK)
    
class RejectDoctor(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email field is required'}, status=status.HTTP_400_BAD_REQUEST)
        doctor = CustomUser.objects.filter(email=email, role='doctor').first()
        if not doctor:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        if doctor.is_approved:
            return Response({'error': 'Doctor is already approved'}, status=status.HTTP_400_BAD_REQUEST)
        if doctor.is_rejected:
            return Response({'error':'Doctor is already rejected'},status=status.HTTP_400_BAD_REQUEST)
        
        doctor.is_rejected = True
        doctor.save()
       
        return Response({'message': 'Doctor account rejected successfully'}, status=status.HTTP_200_OK)

    def get(self, request):
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PatientListView(APIView):
    def get(self, request):
        patients = CustomUser.objects.filter(role='patient', is_staff=False)
        serializer = CustomUserSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PatientUpdate(APIView):
    def post(self,request,pk):
        try:
            patient=CustomUser.objects.get(pk=pk)
        except CustomUser.DoesnotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=PatientSerializer(patient,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PatientDelete(APIView):
    def get(self,request,pk):
        try:
            patient=CustomUser.objects.get(pk=pk,deleted=False)
            patient.deleted=True
            patient.save()
        except CustomUser.DoesNotExist:
            return Response({'error':'Patient not found'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'patient soft deleted successfully!!'})

class PatientRestore(APIView):
    def get(self,request,pk):
        try:
            patient=CustomUser.objects.get(pk=pk,deleted=True)
            patient.deleted=False
            patient.save()
            return Response({'message':'patient restored successfully!!'})
        except CustomUser.DoesNotExist:
            return Response({'error':'Patient not found or already restored'},status=status.HTTP_400_BAD_REQUEST)


class AddSpecialisation(APIView):
    def post(self, request):
        print(request.data," dffffffffffffffffffffffffff")
        serializer = SpecialisationSerializer(data=request.data)
        
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SpecialisationRestore(APIView):
    def patch(self, request, pk):
        try:
            spec=DocSpecialisation.objects.get(pk=pk,is_active=False)
            spec.is_active=True
            spec.save()
        except DocSpecialisation.DoesNotExist:
            return Response({'error':'specialisation not found'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'specialisation restored successfully!!'})


class SpecialisationDelete(APIView):
    def patch(self,request,pk):
        try:
            spec=DocSpecialisation.objects.get(pk=pk,is_active=True)
            spec.is_active=False
            spec.save()
            return Response({'message':'specialisation decativated successfully!!'})
        except DocSpecialisation.DoesNotExist:
            return Response({'error':'specialisation not found or already activated'},status=status.HTTP_400_BAD_REQUEST)

# class SpecialisationListView(ListAPIView):
#     queryset = specialisation.objects.all()
#     serializer_class = SpecialisationSerializer
    
class SpecialisationViewSet(ModelViewSet):
    queryset = DocSpecialisation.objects.all()
    serializer_class = SpecialisationSerializer

# class SpecialisationListDetail(RetrieveAPIView):
#     queryset = specialisation.objects.all()
#     serializer_class = SpecialisationSerializer
    

class DoctorListView(APIView):
    def get(self, request):
        doctors = CustomUser.objects.filter(role='doctor', is_staff=False)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddPost(APIView):
    def post(self,request):
        serializer=BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewPost(APIView):
      def get(self, request):
        blogs = BlogPost.objects.filter(is_verified=True)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class ViewDoctorblog(APIView):
    def get(self,request):
        # blog = BlogPost.objects.exclude(created_by='admin@medico')
        blog=BlogPost.objects.exclude(is_verified='True')
        serializer=BlogSerializer(blog,many=True)
        return Response(serializer.data)
    

class ApproveDoctorBlog(APIView):
    def post(self,request):
        data=request.data
        print(data,"-----dta------------")
        try:
            blog_id=request.data.get('blog_id')
            if not blog_id:
               return Response({'error':'blog id is required!!'})

            blog=BlogPost.objects.get(pk=blog_id)
            blog.is_verified=True
            blog.save()
            return Response({'message':'Blog post approved successfully!!'})
        except BlogPost.DoesNotExist:
            return Response({'error':'Blog post not found'})
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class blogDelete(APIView):
    def get(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk,is_active=True)
            blog.is_active=False
            blog.save()
            return Response({'message':'Blog deactivated successfully!!'},status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'error':'blog not found or already activated'},status=status.HTTP_400_BAD_REQUEST)

class blogRestore(APIView):
    def get(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk,is_active=False)
            blog.is_active=True
            blog.save()
            return Response({'message':'blog restored successfully'},status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response({'error':'error restoring blog'},status=status.HTTP_400_BAD_REQUEST)
        

class BlogEdit(APIView):
    def get(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk)
            serializer=BlogEditSerializer(blog)
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
    def patch(self,request,pk):
        try:
            blog=BlogPost.objects.get(pk=pk)
            serializer = BlogEditSerializer(blog, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

