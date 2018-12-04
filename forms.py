from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('id', 'pw', 'uname', 'phone_num', 'user_type',)

class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('id', 'pw')