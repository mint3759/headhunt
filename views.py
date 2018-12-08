from django.shortcuts import render, redirect
from .models import Users
from .forms import *
from django.forms.utils import ErrorList
from django.db import connection
from django.contrib import messages
import base64
import hashlib

# Create your views here.

def index(request):
    users = Users.objects.all()
    return render(request, 'headhunt/index.html', {'users': users})

def register(request):
    return render(request, 'registration/register.html', {})

def register_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                encrypt_pw = base64.b64encode(hashlib.sha256(form.cleaned_data['pw'].encode()).digest()).decode()
                phone_num = form.cleaned_data['phone_num_0'] + form.cleaned_data['phone_num_1'] + form.cleaned_data['phone_num_2']
                cursor.execute("INSERT INTO USERS (Id, Pw, Is_admin, UName, Phone_num, User_type) VALUES ('"
                               + str(form.cleaned_data['id']) + "', '" + str(encrypt_pw) + "', "
                               + "False" + ", '" + str(form.cleaned_data['uname']) + "', '" + str(phone_num)
                               + "', " +  "'c'" + ")")
                cursor.execute("INSERT INTO CLIENTS VALUES ('" + str(form.cleaned_data['id']) + "')")
                rows = cursor.fetchall()
            return redirect('/registration/register_success')
    else:
        form = ClientForm()
    return render(request, 'registration/register_client.html', {'form': form})

def register(request):
    return render(request, 'registration/register.html', {})

def register_freelancer(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_admin = 0
            #c, f 처리가 필요함
            user.save()
            return redirect('/registration/register_success')
    else:
        form = UserForm()
    return render(request, 'registration/register_freelancer.html', {'form': form})

def register_success(request):
    return render(request, 'registration/register_success.html', {})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                id = form.cleaned_data['id']
                encrypt_pw = base64.b64encode(hashlib.sha256(form.cleaned_data['pw'].encode()).digest()).decode()
                cursor.execute("SELECT PW FROM USERS WHERE ID='" + form.cleaned_data['id'] + "'")
                rows = cursor.fetchone()
                if rows is None:
                    messages.info(request, '아이디가 없거나 비밀번호가 틀렸습니다.')
                    return redirect('/accounts/login/')
                elif encrypt_pw == rows[0]:
                    request.session['login'] = True
                    request.session['id'] = id
                    return redirect('/')
                else:
                    messages.info(request, '아이디가 없거나 비밀번호가 틀렸습니다.')
                    return redirect('/accounts/login/')
        messages.info(request, '유효한 ID와 비밀번호를 입력하세요.')
        return redirect('/accounts/login/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    del request.session['login']
    del request.session['id']
    return render(request, 'registration/logged_out.html', {})