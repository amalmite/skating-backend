from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from .models import *
from .forms import *
from django.core.mail import send_mail
from rest_framework.serializers import ValidationError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from random import randint
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from icerink.settings import ALLOWED_HOSTS
from django.contrib import messages

# Create your views here.

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.views.generic import TemplateView
from web_project import TemplateLayout
from datetime import date
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
from web_project import TemplateLayout



class SessionCreateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        session_form = SessionForm()
        hourly_session_form = HourlySessionForm()
        membership_session_form = MembershipSessionForm()
        context['session_form'] = session_form
        context['hourly_session_form'] = hourly_session_form
        context['membership_session_form'] = membership_session_form
        return context

    def post(self, request, *args, **kwargs):
        session_form = SessionForm(request.POST, request.FILES)
        hourly_session_form = HourlySessionForm(request.POST)
        membership_session_form = MembershipSessionForm(request.POST)

        if session_form.is_valid():
            session = session_form.save(commit=False)
            session_type = session_form.cleaned_data['session_type']
            session.save()  

            if session_type == 'hour':
                if hourly_session_form.is_valid():
                    hour_session = hourly_session_form.save(commit=False)
                    hour_session.session = session
                    hour_session.save()
                    messages.success(request, 'Hourly session added successfully.')
                    return redirect('session_list')
            elif session_type == 'month':
                if membership_session_form.is_valid():
                    membership_session = membership_session_form.save(commit=False)
                    membership_session.session = session
                    membership_session.save()
                    messages.success(request, 'Membsership session added successfully.')
                    return redirect('session_list')
            else:
                messages.error(request, 'Session creation failed.Enter valid data')
                return redirect('session_create')
        else:
            messages.error(request, 'Session creation failed.Enter valid data')
            return redirect('session_create')  
          
    

class SessionListView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        sessions = self.get_total_sessions()
        context.update({
            "sessions": sessions,
            "session_count": sessions.count(),
            "membership_session_count": self.get_total_membership_sessions(),
            "hour_session_count": self.get_total_hourly_sessions(),
            "canceled_session_count": self.get_total_canceled(),
        })
        print('status',sessions.values_list('status'))
        return context

    def get_total_sessions(self):
        return Session.objects.all().order_by('id')
    
    def get_total_hourly_sessions(self):
        return Session.objects.filter(session_type='hour').count()
    
    def get_total_membership_sessions(self):
        return Session.objects.filter(session_type='month').count()

    def get_total_canceled(self):
        return Session.objects.filter(status=False).count()



class SessionUpdateView(TemplateView):
    def get_context_data(self,id, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        session = get_object_or_404(Session, pk=id)
        session_form = SessionUpdateForm(instance=session)
        if session.session_type == 'hour':
            hourly_session_form = HourlySessionForm( instance=session.hourlysession or None)
            membership_session_form = MembershipSessionForm()
        elif session.session_type == 'month':
            hourly_session_form = HourlySessionForm()
            membership_session_form = MembershipSessionForm( instance=session.membershipsession or None)
        context['session_form'] = session_form
        context['hourly_session_form'] = hourly_session_form
        context['membership_session_form'] = membership_session_form
        return context
    

    
    def post(self, request, id,*args, **kwargs):
        session = get_object_or_404(Session, pk=id)
        session_form = SessionUpdateForm(request.POST, request.FILES, instance=session)
        if session.session_type == 'hour':
            hourly_session_form = HourlySessionForm(request.POST, instance=session.hourlysession or None)
            membership_session_form = MembershipSessionForm()
        elif session.session_type == 'month':
            hourly_session_form = HourlySessionForm()
            membership_session_form = MembershipSessionForm(request.POST, instance=session.membershipsession or None)

        if session_form.is_valid():
            session = session_form.save(commit=False)
            session.save()
            if session.session_type == 'hour':
                if hourly_session_form.is_valid():
                    hourly_session = hourly_session_form.save(commit=False)
                    hourly_session.save()
            elif session.session_type == 'month':
                if membership_session_form.is_valid():
                    membership_session = membership_session_form.save(commit=False)
                    membership_session.save()
            messages.success(request, 'Session updated successfully.')
            return redirect('session_list')  
        else:
            messages.error(request, 'Session updated failed . Enter valid data')
            return redirect('session_update',id=id)  


class ProductCreateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        product_form = ProductForm()
        context['product_form'] = product_form
        return context

    def post(self, request, *args, **kwargs):
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Product added successfully.')

            return redirect('product_list')
        else:
            messages.error(request, 'Failed to add product. Please enter valid data.')
            return redirect('product_create')

class ProductListView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        products = self.get_total_products()
        context.update({
            "products": products,
            "product_count": products.count(),
            "available_products": self.get_total_available_products(),
            "canceled_products": self.get_total_canceled(),
            "rental_products": self.get_total_rent(),

        })
        return context

    def get_total_products(self):
        return Product.objects.all().order_by('id')
    
    def get_total_available_products(self):
        return Product.objects.filter(status=True).count()
    
    def get_total_canceled(self):
        return Product.objects.filter(status=False).count()
    
    def get_total_rent(self):
        return Product.objects.filter(is_rent=True).count()


class ProductUpdateView(TemplateView):

    def get_context_data(self, id,**kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        product = get_object_or_404(Product,id=id)
        product_form = ProductUpdateForm(instance=product)
        context['product_form'] = product_form
        return context

    def post(self, request,id, *args, **kwargs):
        product = get_object_or_404(Product,id=id)

        product_form = ProductUpdateForm(request.POST, request.FILES,instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Product updated successfully.')

            return redirect('product_list')
        else:
            messages.error(request, 'Failed to update product. Please enter valid data.')
            return redirect('product_update',id=id)




class testView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


    
class HeaderForm(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
    
    
class SessionSchedule( TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
    






class TransactionAddView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['current_date'] = date.today().strftime("%Y-%m-%d")
        return context

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            if not self.transaction_exists(form.cleaned_data):
                form.save()
                messages.success(request, 'Transaction Added')
            else:
                messages.error(request, 'Transaction already exists')
        else:
            messages.error(request, 'Transaction Failed')
        return redirect('index')

    def transaction_exists(self, cleaned_data):
        return Transaction.objects.filter(
            customer__iexact=cleaned_data['customer'],
            transaction_date=cleaned_data['transaction_date'],
            due_date=cleaned_data['due_date'],
            total=cleaned_data['total'],
            status=cleaned_data['status']
        ).exists()

def index(request):
    return HttpResponse('hello')

def dashboard_crm(request):
    return HttpResponse('hello')

def logout_admin(request):
    logout(request)
    return redirect('index') 






from django.shortcuts import render, redirect, get_object_or_404


# def SessionDelete(request,id):
#     session = get_object_or_404(Session,id=id)
#     session.delete()
#     messages.success(request, 'Session Deleted')
#     return redirect('list_session')








# def create_session(request):
#     if request.method == 'POST':
#         session_form = SessionCreateForm(request.POST, request.FILES)
#         hourly_session_form = HourlySessionForm(request.POST)
#         membership_session_form = MembershipSessionForm(request.POST)

#         if session_form.is_valid():
#             session = session_form.save()
#             session_type = session_form.cleaned_data['session_type']
#             if session_type == 'hour':
#                 if hourly_session_form.is_valid():
#                     hour_session = hourly_session_form.save(commit=False)
#                     hour_session.session = session
#                     hour_session.save()
#             elif session_type == 'month':
#                 if membership_session_form.is_valid():
#                     membership_session = membership_session_form.save(commit=False)
#                     membership_session.session = session
#                     membership_session.save()
#             return redirect('/') 
#     else:
#         session_form = SessionCreateForm()
#         hourly_session_form = HourlySessionForm()
#         membership_session_form = MembershipSessionForm()
#     return render(request, 'session.html', {'session_form': session_form, 'hourly_session_form': hourly_session_form, 'membership_session_form': membership_session_form})



# Employee & Use API

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
            print(activation_code,'code')
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
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserDataSerializer(user)
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
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_404_NOT_FOUND, 
                )

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://localhost:3000/reset-password/{uidb64}/{token}/" 
            subject = "Forgot Password"
            message = f"Click the link to reset your password: {reset_link}"
            to_email = user.email
            try:
                send_mail(subject, message, None, [to_email])
            except Exception as e:
                return Response(
                    {"error": "Failed to send password reset email"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response(
                {"detail": "Password reset email sent successfully"},
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
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



class EmployeeLoginApiView(APIView):

    serializer_class = EmployeeLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserDataSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# class SkatingProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = SkatingProductSerializer




from rest_framework.decorators import api_view
@api_view(['GET'])
def getRoutes(request):
    routes = {
        "login": request.build_absolute_uri('/api/login/'),
        "register": request.build_absolute_uri('/api/user/register/'),
        "profile": request.build_absolute_uri('/api/user/profile/')
    }
    return Response(routes)


# from .serializers import *

# class UserLoginAPIVew(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data.get("email", None)
#             username = serializer.validated_data.get("username", None)
#             password = serializer.validated_data["password"]

#             custom_token_serializer = MyTokenObtainPairSerializer()

#             if email is not None:
#                 user = authenticate(request, email=email, password=password)
#                 if user is not None:
#                     token = custom_token_serializer.get_token(user)
#                     return Response(
#                         {
#                             "mes": "User Log in Successfully",
#                             "jwt_token": {
#                                 "access": str(token.access_token),
#                                 "refresh": str(token),
#                             },
#                             # "data": UserSerializer(user).data,
#                         },
#                         status=status.HTTP_200_OK,
#                     )
#                 return Response(
#                     {"msg": "User Not Found"}, status=status.HTTP_404_NOT_FOUND
#                 )

#             if username is not None:
#                 user = authenticate(request, username=username, password=password)
#                 if user is not None:
#                     token = custom_token_serializer.get_token(user)
                    
#                     return Response(
#                         {
#                             "mes": "User Log in Successfully",
#                             "jwt_token": {
#                                 "access": str(token.access_token),
#                                 "refresh": str(token),
#                             },
#                             # "data": UserSerializer(user).data,
#                         },
#                         status=status.HTTP_200_OK,
#                     )
#                 # raise AuthenticationFailed("There is no User")
#             return Response(
#                 {"msg": "There is n   o valid Credentials"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# from datetime import timedelta,datetime

# class CreateSessionAPIView(APIView):
#     def get(self,request):
#         data =SessionScheduling.objects.all()
#         serializers=SessionSchedulingSerializer(data,many=True)
#         return Response(serializers.data)
    
#     def post(self, request):
#         serializer = SessionSchedulingSerializer(data=request.data)
#         if serializer.is_valid():
#             from_date = serializer.validated_data['from_date']
#             to_date = serializer.validated_data['to_date']
#             start_time = serializer.validated_data['start_time']
#             end_time = serializer.validated_data['end_time']
#             no_of_slot = serializer.validated_data['no_of_slot']
#             delta = timedelta(days=1)
#             current_date = from_date
#             start_datetime = datetime.combine(datetime.today(), start_time)
#             while current_date <= to_date:
#                 for i in range(no_of_slot):
#                     session_start_time = start_datetime + timedelta(hours=i)
#                     session_end_time = session_start_time + timedelta(hours=1)
#                     session = SessionScheduling.objects.create(
#                         from_date=current_date,
#                         to_date=current_date,
#                         start_time=session_start_time.time(),  
#                         end_time=session_end_time.time(), 
#                     )
#                     session.save()
#                 current_date += delta
#             return Response(status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request):
#         SessionScheduling.objects.all().delete()
#         return Response({"message": "deleted"}, status=status.HTTP_204_NO_CONTENT)
