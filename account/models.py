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



class Role(models.Model):
    name = models.CharField(max_length=255)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, default=None, null=True)
    is_employee = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)



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
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email_activation = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, null=True, blank=True)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100)
    gender = models.CharField(max_length=5)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, default=None, null=True)
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