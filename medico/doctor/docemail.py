from django.core.mail import send_mail
from django.conf import settings
import random
from patient.models import *
from django.core.mail  import EmailMessage
import re  # regular expressions

def sent_otp_email(email):
    print(email)
    try:
        subject = "Your OTP for login"
        otp = random.randint(10000,99999)
        print("............",otp)
        message = f'Your OTP is: {otp}'
        from_email = settings.EMAIL_HOST_USER 
        print(from_email,"testinmg from email>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        send_mail(subject, message, from_email, [email])
        # Update user object with OTP
        user_obj = CustomUser.objects.get(email=email)
        user_obj.otp = otp
        print(user_obj.otp,"....................")
        print("kkkkkkk",user_obj)
        user_obj.save()     
        print("OTP email sent successfully")
    except Exception as e:
        print(f"Error sending OTP email: {e}")

def is_valid_email(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):
        return True
    else:
        return False
    

def send_mail_func(email):
    print("task Started")
    print(email)
    users = CustomUser.objects.filter(is_superuser=False).order_by('-id').first()
    print(users)
    if users:
        Subject = "Welcome to Medico"
        message = f"Hii {users.first_name} Thank you for signing up on Medico.Your Account is now on verification. After verification we'll sent you a confirmation mail.Then you account will be activated. "
        from_email = settings.EMAIL_HOST_USER
        send_mail(Subject, message, from_email, [email])
    return 'done'