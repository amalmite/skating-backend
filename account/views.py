from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import (
    UserRegisterSerializer,
    AccountActivationSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    PasswordResetSerializer,
    LoginSerializer,
    ChangeEmailSerializer,
    ChangeEmailVerifySerializer,
    EmployeeRegistrationSerializer,
    EmployeeSerializer,
)
from .models import AccountActivation, User, Employee
from django.core.mail import send_mail
from rest_framework.serializers import ValidationError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from random import randint

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class UserRegisterView(APIView):

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_user = True
            user.save()
            email_code = AccountActivation(user=user)
            activation_code = email_code.create_confirmation()
            try:
                subject = "Registration OTP"
                message = f"Your OTP for registration is: {activation_code}"
                to_email = user.email
                send_mail(subject, message, None, [to_email])
                return Response({"message": "OTP sent"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"message": f"Failed to send OTP: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActivationView(APIView):

    serializer_class = AccountActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            activation_code = serializer.validated_data.get("code")
            try:
                email_confirmation = AccountActivation.objects.get(
                    activation_code=activation_code
                )

                if email_confirmation.verify_confirmation(activation_code):

                    return Response(
                        {"message": "Account Activated. Proceed To Log in"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Invalid confirmation code."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except AccountActivation.DoesNotExist:
                return Response(
                    {"error": "Invalid confirmation code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer


    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, *args, **kwargs):
        try:
            user = self.request.user
            serializer = self.serializer_class(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            raise ValidationError(serializer.errors)

        except ValidationError as validation_error:
            return Response(
                {"error": "Validation error", "detail": validation_error.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePasswordView(APIView):

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                {"message": "Password changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):

    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except user.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://127.0.0.1:8000/reset-password/{uidb64}/{token}/"
        subject = "Forgot Password"
        message = f"Click the link to reset your password: {reset_link}"
        to_email = user.email
        send_mail(subject, message, None, [to_email])
        return Response(
            {"detail": "Password reset email sent successfully"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    serializer_class = PasswordResetSerializer

     
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            user = None
        if user and default_token_generator.check_token(user, token):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get("new_password")
                user.set_password(new_password)
                user.save()
                return Response(
                    {"detail": "Password reset successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangeEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            new_email = serializer.validated_data["email"]

            if new_email != user.email:
                raise ValidationError(
                    "Provided email doesn't match the logged-in user's email."
                )

            code = str(randint(100000, 999999))
            user.email_verification_code = code
            user.save()
            subject = "Confirm Email Change"
            message = f"Your email verification code is: {code}"
            from_email = "Your Email"
            to_email = user.email
            send_mail(subject, message, from_email, [to_email], fail_silently=True)
            return Response(
                {"message": "Email change request sent successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailVerifyView(APIView):

    serializer_class =ChangeEmailVerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            code = serializer.validated_data["code"]
            new_email = serializer.validated_data["new_email"]

            if user.email_verification_code == code:
                user.email = new_email
                user.email_verification_code = None
                user.save()
                return Response(
                    {"success": "Email changed successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid or expired verification code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Employee registeration
class EmployeeRegistrationAPIView(APIView):
     
    serializer_class = EmployeeRegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registeration Sucessfull"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Employee Profile
class EmployeeProfileAPiView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(user=request.user)
            serializer = self.serializer_class(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
