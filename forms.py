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

class MakeRequestForm(forms.Form):
    reqtitle = forms.CharField()
    fund = forms.IntegerField()
    min_exp = forms.IntegerField()
    min_fre = forms.IntegerField()
    max_fre = forms.IntegerField()

class FreelancerForm(forms.Form):
    id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    pw = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    uname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_0 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    age = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    exp = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    major = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )

    language = forms.CharField()