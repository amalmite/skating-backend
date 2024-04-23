from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate



class EmployeeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['job_role', 'employee_id']

class UserDataSerializer(serializers.ModelSerializer):
    employee = EmployeeDataSerializer(required=False)
    class Meta:
        model = User
        fields = ['email','username','first_name','last_name','is_user','is_admin','is_employee','employee']



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        user = User.objects.create_user(**validated_data)
        return user


class AccountActivationSerializer(serializers.Serializer):
    code = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_user and user.is_active and user.email_activation:
            return user
        raise serializers.ValidationError("Incorrect username or password.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "phone_number",
            "first_name",
            "last_name",
       
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.phone = validated_data.get("phone_number", instance.phone_number)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"error": "Password fields didn't match."}
            )
        return attrs


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangeEmailVerifySerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        if User.objects.filter(email=attrs).exists():
            raise serializers.ValidationError("Email already exists.")
        return attrs


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Employee
        fields = [
            "user",
            "employee_id",
            "nationality",
            "gender",
            "business_profile",
            "job_role",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserRegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.is_employee = True
            user.save()
            employee = Employee.objects.create(user=user, **validated_data)
            return employee
        else:
            raise serializers.ValidationError(user_serializer.errors)



class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = "__all__"

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_instance = instance.user
            user_instance.username = user_data.get("username", user_instance.username)
            user_instance.first_name = user_data.get(
                "first_name", user_instance.first_name
            )
            user_instance.last_name = user_data.get(
                "last_name", user_instance.last_name
            )
            user_instance.phone_number = user_data.get(
                "phone_number", user_instance.phone_number
            )
            user_instance.save()

        instance.employee_id = validated_data.get("employee_id", instance.employee_id)  
        instance.nationality = validated_data.get("nationality", instance.nationality)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.save()

        return instance



class EmployeeLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and user.is_employee:
            return user
        raise serializers.ValidationError("Incorrect username or password.")


# class SkatingProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields="__all__"

# class SessionSchedulingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SessionScheduling
#         fields = '__all__'


# login

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.tokens import RefreshToken


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = RefreshToken.for_user(user)
#         token["email"] = user.email
#         token["first_name"] = user.first_name
#         token["is_active"] = user.is_active
#         return token
    
# class UserLoginSerializer(serializers.Serializer):
#     email =serializers.CharField(required=False)
#     username = serializers.CharField(required=False)
#     password = serializers.CharField(style={"input_type": "password"})
