from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.core.mail import send_mail
import os
import logging


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
# role model
class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.description}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    #  this profile supervisor
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervisor_profiles')
    birthday = models.DateField(null=True, blank=True)
    # use this image url as a default https://img.freepik.com/free-vector/man-profile-account-picture_24908-81754.jpg?w=826&t=st=1710450387~exp=1710450987~hmac=5371500fb04f8770784bc3b434179fc06ff8ae0bd7d4fe480f3358bdb53f62bf
    image = models.ImageField(default='profile_pics/default.webp', upload_to='profile_pics')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    # each profile can have multiple roles
    roles = models.ManyToManyField(Role, related_name='profiles', blank=True)


    def __str__(self):
        return f"{self.user.username} profile"


    # send email with the code
    def send_code(self, code):
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')
        user_email = self.user.email

        subject = f' New code generated for {self.user.username}'
        message = f' You are now able to log in with the code {code}'

        try:
            send_mail(subject, message, email_user, [user_email], auth_user=email_user, auth_password=email_password)
            logging.info(f'Successfully sent code to {user_email}')
        
        except Exception as e:
            logging.error(f'Error sending code to {user_email}: {str(e)}')