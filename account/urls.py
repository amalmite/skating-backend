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
    EmployeeRegistrationAPIView,
    EmployeeProfileAPiView,
    EmployeeLoginApiView,
    EmployeeListView,
    SkatingProductViewSet,getRoutes,CreateSessionAPIView)
from .views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'products', SkatingProductViewSet)



urlpatterns = [
    path('',testView.as_view(template_name="test.html"),name="test"),
    # path('header_form/',HeaderForm.as_view(template_name="header_form.html"),name="header-form"),




    path('inedx/',index,name="index"),
    path('dashboard/',dashboard_crm,name="dashboard-crm"),
    path('logout/',logout_admin,name="logout"),



    path('api/product', include(router.urls)),
    path("api/user/register/", UserRegisterView.as_view(), name="user_register"),
    path("api/activation/", AccountActivationView.as_view(), name="account_activation"),
    path("api/login/", Login.as_view(), name="login"),
    path("api/user/profile/", UserDetailAPIView.as_view(), name="profile"),
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
    path(
        "api/employee/register/",
        EmployeeRegistrationAPIView.as_view(),
        name="employee_register",
    ),
    path(
        "api/employee/profile/",
        EmployeeProfileAPiView.as_view(),
        name="employee_profile",
    ),
    path(
        "api/employee/login/",
        EmployeeLoginApiView.as_view(),
        name="employee_login",
    ),
    path(
        "api/employee/login/",
        EmployeeLoginApiView.as_view(),
        name="employee_login",
    ),
    path("api/employee/list/", EmployeeListView.as_view(), name="employee_list"),

    path("api/session/", CreateSessionAPIView.as_view(), name="employee_list"),

    path("api/", getRoutes)


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)