from django.urls import path, include
from .views import UserRegisterView,AccountActivationView,MyObtainTokenPairView

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'User', UserRegisterView)
# router.register(r'AccountActivation', AccountActivationView)



urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("activation/", AccountActivationView.as_view(), name="account_activation"),
    path("login/", MyObtainTokenPairView.as_view(), name="login"),
    # path('', include(router.urls)), 


]