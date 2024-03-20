from django.core.mail import send_mail
from django.conf import settings
import random
from .models import *
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
    

def send_mail_func(self):
    print("task Started")
    users = CustomUser.objects.filter(is_superuser=False).order_by('-id').first()
    print(users)
    if users:
        Subject = "Welcome to Medico"
        message = f"Hii {users.first_name} thanks for signing up on Medico "
        from_email = settings.EMAIL_HOST_USER
        d_mail = EmailMessage(subject=Subject, body= message, from_email=from_email, to=[users.email])
        d_mail.send(fail_silently=False)
    return 'done'