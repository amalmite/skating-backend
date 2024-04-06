from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    # def authenticate(self, request, username=None, password=None, **kwargs):
    #     try:
    #         user = User.objects.get(email=username)
    #     except User.DoesNotExist:

    #         try:
    #             user = User.objects.get(username=username)
    #         except User.DoesNotExist:
    #             return None

    #     if user.check_password(password):
    #         return user
    #     else:
    #         return None

    def authenticate(
        self, request, username=None, email=None, password=None, **kwargs
    ):

        if email:
            print("auth backends EMAIL code")
            try:
                user = User.objects.get(email=email)

                if user.check_password(password):
                    return user
                raise AuthenticationFailed("Password is not Correct")

            except User.DoesNotExist:
                return None
            
        if username:
            try:
                user = User.objects.get(username=username)

                if user.check_password(password):
                    return user
                raise AuthenticationFailed("Password is not Correct")

            except User.DoesNotExist:
                return None
