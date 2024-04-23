from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint
from django.core.exceptions import ValidationError

from location_field.models.plain import PlainLocationField

# Create your models here.

class CompanyGroup(models.Model):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    logo = models.FileField(upload_to='logo/')

    def __str__(self):
        return f"Group dashboard{self.name}"

class Location(models.Model):
    name = models.CharField(max_length=255)
    emirates = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    google_map = PlainLocationField(based_fields=['city'], zoom=7)

    def __str__(self):
        return f"Location {self.name} country {self.country}"

class Mall(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="Mall Location", null=True)
    picture = models.FileField(upload_to='mall/')

    def __str__(self):
        return f"Mall details {self.name} "

class Tax(models.Model):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    tax_percentage_checkbox = models.BooleanField(default=False)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fixed_price_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Tax {self.full_name}"
    
class PaymentMode(models.Model):

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Disabled', 'Disabled'),
    ]

    name = models.CharField(max_length=100)
    wallet_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name
    


class BusinessProfile(models.Model):
    name = models.CharField(max_length=64, blank=False, default=None, null=True)
    mall = models.ForeignKey(Mall,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=25)
    email = models.EmailField()
    currency = models.CharField(max_length=25)
    select_tax = models.ManyToManyField(Tax,default=None)
    trn_no = models.CharField(max_length=20)
    tax_reporting_dates = models.CharField(max_length=100)
    license_no = models.CharField(max_length=50)
    expiry = models.DateField()
    operational_hours_start = models.TimeField()
    operational_hours_end = models.TimeField()
    report_generation_start_time = models.TimeField(default='07:00')
    report_generation_end_time = models.TimeField(default='06:59')
    invoice_heading = models.CharField(max_length=255)
    address = models.TextField()
    logo = models.ImageField(upload_to='logo/')

    def __str__(self):
        return f"Business profile{self.name} {self.mall}"
    

class Module(models.Model):
    URL_CHOICES = [
        ('/product/product/', 'product'),
    ]
    URL_NAMES = [
        ('product Report', '/product/product-report/'),
    ]
    url = models.CharField(max_length=150, choices=URL_CHOICES, null=True, verbose_name='Page Name')
    name = models.CharField(max_length=50, choices=URL_NAMES, null=True, verbose_name='Page URL')
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    ROLE_TYPE_CHOICES = (
        ('Employee', 'Employee'),
        ('Business', 'Business'),
        ('Group', 'Group'),
        ('Django Admin', 'Django Admin'),
    )

    name = models.CharField(max_length=100)
    modules = models.ManyToManyField(Module, default=None)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, default=None, null=True)
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES)

    def __str__(self):
        return self.name


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
    passport_no = models.CharField(max_length=20, unique=True)
    passport_expiration_date = models.DateField()
    emirates_id = models.CharField(max_length=20, unique=True)
    id_expiration_date = models.DateField()
    basic_pay = models.DecimalField(max_digits=10, decimal_places=2)
    house_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transportation_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joining_date = models.DateField()

    def __str__(self):
        return f"Employee: {self.user.username}, Job Role: {self.job_role}"



# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2) 
#     stock = models.IntegerField()
#     picture = models.ImageField(upload_to='products/')  
#     tax = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return self.name
    

# class AdmissionCategory(models.Model):

#     CATEGORY_CHOICES = [
#         ('kids', 'Kids'),
#         ('adult', 'Adult'),
#         ('senior', 'Senior Citizen'),
#     ]

#     category_name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)

#     def __str__(self):
#         return self.category_name


# class SessionType(models.Model):
#     name = models.CharField(max_length=255)

# class Skate(models.Model):
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     duration_hours = models.PositiveIntegerField(default=1)
#     duration_days = models.PositiveIntegerField(default=0)
#     picture1 = models.FileField(upload_to='skate/')
#     picture2 = models.FileField(upload_to='skate/')
#     tax = models.DecimalField(max_digits=5, decimal_places=2)
#     session_type = models.ForeignKey(SessionType,on_delete=models.CASCADE)


#     def __str__(self):
#         return self.name

# class SessionScheduling(models.Model):
#     from_date = models.DateField(null=True)
#     to_date = models.DateField(null=True)
#     start_time = models.TimeField(null =True )
#     end_time = models.TimeField(null=True)
#     no_of_slot = models.PositiveIntegerField(null=True)
#     duration = models.PositiveIntegerField()
#     skate = models.ForeignKey(Skate, on_delete=models.CASCADE)
#     admits = models.PositiveIntegerField(default=70)

#     def __str__(self):
#         return f"{self.from_date} to {self.to_date}"



# class SkateBooking(models.Model):

#     PENDING = 'Pending'
#     CONFIRMED = 'Confirmed'
#     CANCELLED = 'Cancelled'
#     COMPLETED = 'Completed'

#     STATUS_CHOICES = [
#         (PENDING, 'Pending'),
#         (CONFIRMED, 'Confirmed'),
#         (CANCELLED, 'Cancelled'),
#         (COMPLETED, 'Completed'),
#     ]

#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     session = models.ForeignKey(SessionScheduling,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
#     product_quantity = models.PositiveIntegerField(null=True,blank=True)
#     sub_total = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

#     def __str__(self):
#         return f"{self.user.username}'s booking for {self.session} - Status: {self.status}"


class Transaction(models.Model):
    customer = models.CharField(max_length=150)
    transaction_date = models.DateField()
    due_date = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Due", "Due"), ("Canceled", "Canceled")])

    def __str__(self):
        return self.customer

# class Session(models.Model):
#     SESSION_TYPES = (
#         ('hour', 'Hourly'),
#         ('membership', 'Membsership'),
#     )
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=20, decimal_places=2)
#     vat = models.DecimalField(max_digits=5,decimal_places=2)
#     description = models.TextField()
#     image1 = models.FileField(upload_to='session/')
#     image2 = models.FileField(upload_to='session/')
#     session_type = models.CharField(max_length=10, choices=SESSION_TYPES)
#     hour = models.PositiveSmallIntegerField(null=True, blank=True)
#     month = models.PositiveSmallIntegerField(null=True, blank=True)
#     day = models.PositiveSmallIntegerField(null=True, blank=True)
#     membership_total_sessions = models.PositiveIntegerField(null=True, blank=True)
#     # or 

class Session(models.Model):
    SESSION_TYPES = (
        ('hour', 'Hourly'),
        ('month', 'Monthly'),
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    vat = models.DecimalField(max_digits=5,decimal_places=2)
    description = models.TextField()
    image1 = models.FileField(upload_to='session/')
    image2 = models.FileField(upload_to='session/',null=True,blank=True)
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES)
    status = models.BooleanField(default=True)
    

    def __str__(self):
        return f"Session - {self.name} {self.session_type}"

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"



class HourlySession(models.Model):
    session = models.OneToOneField(Session,on_delete=models.CASCADE)
    hour = models.PositiveSmallIntegerField(null=True, blank=True)
    minute = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.session.name} {self.hour}"

class MembershipSession(models.Model):
    session = models.OneToOneField(Session,on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField(null=True, blank=True)
    day = models.PositiveSmallIntegerField(null=True, blank=True)
    total_sessions = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.session.name} {self.month}"




class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')  
    vat = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    is_sale = models.BooleanField(default=False)
    is_rent = models.BooleanField(default=True)
    status = models.BooleanField(default=True)


class HomeAdvertisement(models.Model):
    banner_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_session = models.BooleanField(default=False)
    is_url = models.BooleanField(default=False)
    session = models.ForeignKey(Session,on_delete=models.CASCADE ,null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    button_name = models.CharField(max_length=200)
    image = models.FileField(upload_to='banner/',null=True,blank=True)
    banner_text1 = models.CharField(max_length=200)
    banner_text2 = models.CharField(max_length=200)
    banner_text3 = models.CharField(max_length=200)


class SessionDate(models.Model):
    session = models.ForeignKey(Session,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)


class SessionSchedule(models.Model):
    session_date = models.ForeignKey(SessionDate, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_admissions =models.PositiveBigIntegerField()
