from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint

# Create your models here.


class BusinessProfile(models.Model):
    name = models.CharField(max_length=64, blank=False, default=None, null=True)
    mall = models.CharField(max_length=255)
    # phone_number = models.CharField(max_length=25)
    # email = models.EmailField()
    # currency = models.CharField(max_length=25)
    # address = models.TextField()
    # license_number = models.CharField(max_length=255)

    def __str__(self):
        return f"Business profile{self.name} {self.mall}"


class Role(models.Model):
    name = models.CharField(max_length=255)
    business_profile = models.ForeignKey(
        BusinessProfile, on_delete=models.CASCADE, default=None, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Role profile{self.name}"


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email_activation = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_user = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class AccountActivation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_code = models.CharField(
        max_length=6, null=True, blank=True, verbose_name=("Activation Code")
    )

    def __str__(self):
        return f"Email Confirmation for {self.user.email}"

    def create_confirmation(self):
        code = str(randint(100000, 999999))
        self.activation_code = code
        self.save()
        return code

    def verify_confirmation(self, code):
        if self.activation_code == code:
            self.user.email_activation = True
            self.user.save()
            return True
        return False


class Employee(models.Model):

    NATIONALITY_CHOICES = [
        
        ('UAE', 'United Arab Emirates'),
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('CA', 'Canada'),
        ('IN', 'India'),

    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100,choices=NATIONALITY_CHOICES)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    business_profile = models.ForeignKey(
        BusinessProfile, on_delete=models.CASCADE, default=None, null=True
    )
    job_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    # passport_no = models.CharField(max_length=20, unique=True)
    # passport_expiration_date = models.DateField()
    # emirates_id = models.CharField(max_length=20, unique=True)
    # id_expiration_date = models.DateField()
    # basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    # house_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # transportation_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # commission_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # joining_date = models.DateField()

    def __str__(self):
        return f"Employee: {self.user.username}, Job Role: {self.job_role}"



class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.IntegerField()
    picture = models.ImageField(upload_to='products/')  
    tax = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

