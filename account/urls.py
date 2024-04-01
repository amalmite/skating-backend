from django.urls import path, include
from .views import UserRegisterView,AccountActivationView,MyObtainTokenPairView,UserDetailAPIView,ChangePasswordView,ForgotPasswordView,ResetPasswordView

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'User', UserRegisterView)
# router.register(r'AccountActivation', AccountActivationView)



urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user_register"),
    path("activation/", AccountActivationView.as_view(), name="account_activation"),
    path("login/", MyObtainTokenPairView.as_view(), name="login"),
    path("profile/", UserDetailAPIView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/<str:uidb64>/<str:token>/", ResetPasswordView.as_view(), name="reset_password"),




    # path('', include(router.urls)), 


]