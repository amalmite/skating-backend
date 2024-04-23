from django import forms
from .models import *

        

class SessionUpdateForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name','status' ,'price', 'vat', 'description', 'session_type','image1','image2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'session name'}),
            'status': forms.Select(choices=((True, 'Active'), (False, 'Inactive')), attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder':'price'}),
            'vat': forms.NumberInput(attrs={'class': 'form-control','placeholder':'vat'}),
            'description': forms.Textarea(attrs={'class': 'form-control h-px-100', 'rows': 3,'placeholder':'Description','maxlength':255}),
            'session_type': forms.RadioSelect(),
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'price', 'vat', 'description', 'session_type','image1','image2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'session name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder':'price'}),
            'vat': forms.NumberInput(attrs={'class': 'form-control','placeholder':'vat'}),
            'description': forms.Textarea(attrs={'class': 'form-control h-px-100', 'rows': 3,'placeholder':'Description','maxlength':255}),
            'session_type': forms.RadioSelect(),
        }

class HourlySessionForm(forms.ModelForm):
    class Meta:
        model = HourlySession
        fields = ['hour', 'minute']
        widgets = {
            'hour': forms.TextInput(attrs={'class': 'form-control','placeholder':'session name','id':'hour_hour'}),
            'minute': forms.NumberInput(attrs={'class': 'form-control','placeholder':'price','id':'hour_minute'}),
        }

class MembershipSessionForm(forms.ModelForm):
    class Meta:
        model = MembershipSession
        fields = ['month', 'day', 'total_sessions']
        widgets = {
            'month': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Month','id':'member_month'}),
            'day': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Day','id':'member_day'}),
            'total_sessions': forms.NumberInput(attrs={'class': 'form-control','placeholder':'Total Session','id':'member_total'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','code','price','description','image','vat','stock']
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'session name'}),
        'code': forms.TextInput(attrs={'class': 'form-control','placeholder':'code'}),
        'description': forms.Textarea(attrs={'class': 'form-control h-px-100', 'rows': 3,'placeholder':'Description','maxlength':255}),
        'price': forms.NumberInput(attrs={'class': 'form-control','placeholder':'price'}),
        'vat': forms.NumberInput(attrs={'class': 'form-control','placeholder':'vat'}),
        'stock': forms.NumberInput(attrs={'class': 'form-control','placeholder':'stock'}),
        }

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','code','price','description','image','vat','stock','status']
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Product name'}),
        'code': forms.TextInput(attrs={'class': 'form-control','placeholder':'code'}),
        'description': forms.Textarea(attrs={'class': 'form-control h-px-100', 'rows': 3,'placeholder':'Description','maxlength':255}),
        'price': forms.NumberInput(attrs={'class': 'form-control','placeholder':'price'}),
        'vat': forms.NumberInput(attrs={'class': 'form-control','placeholder':'vat'}),
        'stock': forms.NumberInput(attrs={'class': 'form-control','placeholder':'stock'}),
        'status': forms.Select(choices=((True, 'Active'), (False, 'Inactive')), attrs={'class': 'form-control'}),

        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'