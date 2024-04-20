from django import forms
from .models import *

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'price', 'vat', 'description', 'session_type']

class HourlySessionForm(forms.ModelForm):
    class Meta:
        model = HourlySession
        fields = ['hour', 'minute']

class MembershipSessionForm(forms.ModelForm):
    class Meta:
        model = MembershipSession
        fields = ['month', 'day', 'total_sessions']