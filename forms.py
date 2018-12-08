from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('id', 'pw', 'uname', 'phone_num', 'user_type',)

class LoginForm(forms.Form):
    id = forms.CharField()
    pw = forms.CharField()

class ClientForm(forms.Form):
    id = forms.CharField()
    pw = forms.CharField()
    uname = forms.CharField()
    phone_num_0 = forms.CharField()
    phone_num_1 = forms.CharField()
    phone_num_2 = forms.CharField()

class FreelancerForm(forms.Form):
    id = forms.CharField()
    pw = forms.CharField()
    uname = forms.CharField()
    phone_num_0 = forms.CharField()
    phone_num_1 = forms.CharField()
    phone_num_2 = forms.CharField()
    age = forms.IntegerField()
    exp = forms.IntegerField()
    major = forms.CharField()
    language = models.CharField()

class ProficiencyForm(forms.Form):
    proficiency = models.DecimalField()

class PortfolioForm(forms.Form):
    portfolio = models.FileField()