from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
from django.core.validators import MaxValueValidator
from datetime import date 


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email =self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email,password,**extra_fields)
    

    
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=30,blank=True)
    last_name=models.CharField(max_length=30,blank=True)
    place=models.CharField(max_length=30,blank=True)
    phone_number = models.CharField(max_length=15, blank=True) 
    age = models.IntegerField(blank=True,null=True) 
    exp = models.IntegerField(blank=True,null=True)  
    # specialisation = models.ForeignKey(Specialisation, on_delete=models.SET_NULL, null=True, blank=True)
    specialisation = models.CharField(max_length=100, blank=True, null=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    is_approved = models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    deleted=models.BooleanField(default=False)
    profile_image=models.ImageField(blank=True,upload_to='profilepic/')
    consultation_fee = models.IntegerField(validators=[MaxValueValidator(2000)],null=True)
    
    objects=CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

class Document(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    experience_certificate = models.ImageField(upload_to='documents/')
    mbbs_certificate = models.ImageField(upload_to='documents/')
    # Add more fields for other certificates/documents as needed

class DocSpecialisation(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title=models.CharField(max_length=500)
    blog_content=models.CharField(max_length=500,null=True)
    article = models.FileField(upload_to='blogpost/', null=True, blank=True)
    video = models.FileField(upload_to='blogpost/', null=True, blank=True)
    created_by=models.CharField(max_length=100,default='admin@medico')
    is_verified=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)

class TimeSlot(models.Model):
    Doctor= models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    start_time = models.TimeField()
    date = models.DateField(null=True,blank=True)
    available = models.BooleanField(default=True,null=True)

class SlotBooking(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_bookings')
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_bookings')
    date = models.DateField()
    start_time = models.TimeField()
    payment_completed=models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.patient} with {self.doctor} at {self.start_time} on {self.date}"
