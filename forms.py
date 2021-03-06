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
                "type": "password",
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
    reqtitle = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    fund = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    min_exp = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            })
    )
    min_fre = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "onchange": "mincheck()"
            })
    )
    max_fre = forms.IntegerField(
        min_value=0,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "onchange": "maxcheck()"
            })
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                'type': 'date',
                "onchange": "fromdatecheck()"
            })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                'type': 'date',
                "onchange": "todatecheck()"

            })
    )
    req_doc = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
            })
    )

    language = forms.CharField()

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
                "type": "password",
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
                "class": "form-control",
                "onchange" : "age_check()"
            })
    )
    exp = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "onchange" : "exp_check()"

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
    portfolio = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
            })
    )

class updateClientForm(forms.Form):
    pw = forms.CharField(
        required=False,
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            })
    )
    uname = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "value": "",
                "class": "form-control"
            })
    )
    phone_num_0 = forms.CharField(
        required=False,
        max_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_1 = forms.CharField(
        required=False,
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_2 = forms.CharField(
        required=False,
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )


class UpdateFreelancerForm(forms.Form):
    pw = forms.CharField(
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "type": "password",
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
                "class": "form-control",
                "onchange" : "age_check()"
            })
    )
    exp = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "onchange" : "exp_check()"

            })
    )
    major = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    portfolio = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
            })
    )

class updateClientForm(forms.Form):
    pw = forms.CharField(
        required=False,
        max_length=16,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            })
    )
    uname = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "value": "",
                "class": "form-control"
            })
    )
    phone_num_0 = forms.CharField(
        required=False,
        max_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_1 = forms.CharField(
        required=False,
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    phone_num_2 = forms.CharField(
        required=False,
        max_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )

class MakeTeamForm(forms.Form):

    tName = forms.CharField(
        max_length = 20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )
    id = forms.CharField(
        max_length = 14,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )

    teammate = forms.CharField()

class MessageForm(forms.Form):
    message = forms.CharField(
        max_length = 1000,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            })
    )