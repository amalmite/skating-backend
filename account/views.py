from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import UserRegisterSerializer,AccountActivationSerializer,MyTokenObtainPairSerializer,UserSerializer
from .models import AccountActivation
from django.core.mail import send_mail
from rest_framework.serializers import ValidationError

from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class UserRegisterView(APIView):

    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_user = True
            user.save()
            email_code =AccountActivation(user=user)
            activation_code=email_code.create_confirmation()
            try:
                subject = 'Registration OTP'
                message = f'Your OTP for registration is: {activation_code}'
                to_email = user.email
                send_mail(subject, message, None, [to_email])
                return Response({"message": "OTP sent"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": f"Failed to send OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActivationView(APIView):
    serializer_class = AccountActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            activation_code = serializer.validated_data.get('code') 
            try: 
                email_confirmation = AccountActivation.objects.get(activation_code=activation_code)

                if email_confirmation.verify_confirmation(activation_code):

                    return Response({'message': 'Account Activated. Proceed To Log in'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)
            except AccountActivation.DoesNotExist:
                return Response({'error': 'Invalid confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


    def put(self, request, *args, **kwargs):
        try:
            user = self.request.user
            serializer = UserSerializer(user, data=request.data, partial=True)

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
