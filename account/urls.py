from django.urls import path, include
from .views import (
    UserRegisterView,
    AccountActivationView,
    UserDetailAPIView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
    Login,
    ChangeEmailVerifyView,
    ChangeEmailView,
    EmployeeRegistrationAPIView
)

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'User', UserRegisterView)
# router.register(r'AccountActivation', AccountActivationView)


urlpatterns = [
    path("api/register/", UserRegisterView.as_view(), name="user_register"),
    path("api/activation/", AccountActivationView.as_view(), name="account_activation"),
    path("api/login/", Login.as_view(), name="login"),
    path("api/profile/", UserDetailAPIView.as_view(), name="profile"),
    path("api/change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("api/forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "api/reset-password/<str:uidb64>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
    path("api/change-email/", ChangeEmailView.as_view(), name="change_email"),
    path(
        "api/change-email/verify/",
        ChangeEmailVerifyView.as_view(),
        name="change_email_verify",
    ),
    path("api/empolyee/register/", EmployeeRegistrationAPIView.as_view(), name="emplpoyee_register"),

]
