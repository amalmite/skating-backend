from django.contrib import admin
from account.models import User, AccountActivation, Employee, BusinessProfile, Role

# Register your models here.


admin.site.register(User)
admin.site.register(AccountActivation)
admin.site.register(BusinessProfile)
admin.site.register(Role)
admin.site.register(Employee)
