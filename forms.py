from django import forms
from .models import *

class LoginForm(forms.Form):
    id = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    pw = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control"
            })
    )

class ClientForm(forms.Form):
    id = forms.CharField(
        max_length=14,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    pw = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    uname = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_0 = forms.CharField(
        max_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_1 = forms.CharField(
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_2 = forms.CharField(
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )

class MakeRequestForm(forms.Form):
    reqtitle = forms.CharField()
    fund = forms.IntegerField()
    min_exp = forms.IntegerField()
    min_fre = forms.IntegerField()
    max_fre = forms.IntegerField()

class FreelancerForm(forms.Form):
    id = forms.CharField(
        max_length = 14,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    pw = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    uname = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_0 = forms.CharField(
        max_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_1 = forms.CharField(
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_2 = forms.CharField(
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    age = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    exp = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    major = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )

    language = forms.CharField()