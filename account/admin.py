from django.contrib import admin
from account.models import *

# Register your models here.


admin.site.register(User)
admin.site.register(AccountActivation)
admin.site.register(BusinessProfile)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Transaction)
admin.site.register(Session)
admin.site.register(HourlySession)
admin.site.register(MembershipSession)
admin.site.register(Product)