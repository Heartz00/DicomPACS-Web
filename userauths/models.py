from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save
from django.core.mail import send_mail
from dicom.models import Institution  # Import your Institution model


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)  # New field for approval status

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'institution']

    def __str__(self):
        return self.username


    def get_institution(self):
        return self.profile.institution if hasattr(self, 'profile') else None


    def send_approval_email(self):
        # Method to send approval email
        send_mail(
            'Account Approved',
            'Your account has been approved. You can now log in.',
            'oladeleayomide831@gmail.com',  # Replace with your email or settings.DEFAULT_FROM_EMAIL
            [self.email],
            fail_silently=False,
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True) 
    address = models.CharField(max_length=200, null=True, blank=True) 
    country = models.CharField(max_length=200, null=True, blank=True) 
    verified = models.BooleanField(default=False, null=True, blank=True)
    institution = models.CharField(max_length=100, choices=[
        ('Crest View', 'Crest View'),
        ('All Saint Clinic', 'All Saint Clinic'),
        ('NOHL', 'NOHL'),
    ], null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.bio} - {self.institution}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    
class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200) 
    subject = models.CharField(max_length=200) 
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

 
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)    



