
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """custom user Manger"""

    def create_user(self, email, password=None, password2=None, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # user = CustomUser(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        print(f'form user - {user}')
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Coustom user fields"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    mobile=models.CharField(max_length=16,null=False,blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name}-{self.last_name}"
    


class State(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, related_name='districts', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


# Patient registration model 

class PatientRegistration(models.Model):
    

    DEPARTMENTS = [

        ('CLINICAL MEDICINE', 'Clinical Medicine'),
        ('PATHOLOGY', 'Pathology'),
        ('IMMUNOLOGY', 'Immunology'),
        ('MOLECULAR BIOLOGY', 'Molecular Biology'),
        ('BIOCHEMISTRY', 'Biochemistry'),
    ]


    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
        ('PREFER_NOT_TO_SAY', 'Prefer not to say'),
    ]


    CONSULTATION_CHOICES = [
        ('OPD', 'OPD'),
        ('FOLLOW_UP', 'Follow Up')
    ]

   
    name=models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,default='PREFER_NOT_TO_SAY')
    # age = models.IntegerField(blank=False)  
    age = models.IntegerField(null=True, blank=True)

    email=models.EmailField(null=True,blank=True)
    contact_number=models.CharField(max_length=50,blank=True,null=True)
    aadhar_number=models.BigIntegerField(blank=True,null=True)

   # Assuming the State with name "Bihar" has ID 1
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)

    address = models.TextField(help_text="Enter the patient's address here...")
    department=models.CharField(max_length=50,choices=DEPARTMENTS,default='CLINICAL MEDICINE')
    symptoms=models.TextField(help_text='Write about your concerns',null=True, blank=True)
    consultation_type = models.CharField(max_length=20,choices=CONSULTATION_CHOICES,default='OPD')
    appointment_date = models.DateField(
        help_text="Select the appointment date and time",
    )
    registration_date_time=models.DateTimeField(auto_now_add=True)
    registered_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # If age is 0, set it to None
        if self.age == 0:
            self.age = None
        super().save(*args, **kwargs)  # Call the original save method

    
    def __str__(self):
        return f"{self.name} - {self.department}"
    

