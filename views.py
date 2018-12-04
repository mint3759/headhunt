from django.shortcuts import render, redirect
from .models import Users
from .forms import *

# Create your views here.

def index(request):
    users = Users.objects.all()
    return render(request, 'headhunt/index.html', {'users': users})

def register(request):
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
    return render(request, 'registration/register.html', {'form': form})

def register_success(request):
    return render(request, 'registration/register_success.html', {})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    return render(request, 'registration/logged_out.html', {})