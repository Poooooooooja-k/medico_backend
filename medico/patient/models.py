from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
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
    
class Specialisation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
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
    specialisation = models.ForeignKey(Specialisation, on_delete=models.SET_NULL, null=True, blank=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    is_approved = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='doc_image')
    experience_certificate = models.ImageField(upload_to='documents/')
    mbbs_certificate = models.ImageField(upload_to='documents/')
    # Add more fields for other certificates/documents as needed


