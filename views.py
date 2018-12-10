from django.shortcuts import render, redirect
from .models import Users
from .forms import *
from django.forms.utils import ErrorList
from django.db import connection
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
import base64
import hashlib

# Create your views here.

def index(request):
    with connection.cursor() as cursor:
        cursor.execute("Select Id, UName, User_type from Users")
        rows = cursor.fetchall()
        print(rows)
    context = {"home_page": "active"}
    return render(request, 'headhunt/index.html', {'users': rows}, context)

def register(request):
    return render(request, 'registration/register.html', {})

def register_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # id, pw, uname, phone_num_0~2
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
        form = FreelancerForm(request.POST)
        print(form)
        if form.is_valid():
            #id, pw, uname, phone_num_0~2, age, exp, major, lanauage
            tmplangList = form.cleaned_data['language'].split(", ")
            langName = []
            rating = []
            for langs in tmplangList:
                if langs == 'dummy':
                    break
                tmpName, tmpRating = langs.split(":")
                langName.append(tmpName)
                rating.append(tmpRating)
            with connection.cursor() as cursor:
                encrypt_pw = base64.b64encode(hashlib.sha256(form.cleaned_data['pw'].encode()).digest()).decode()
                phone_num = form.cleaned_data['phone_num_0'] + form.cleaned_data['phone_num_1'] + form.cleaned_data['phone_num_2']
                cursor.execute("INSERT INTO USERS (Id, Pw, Is_admin, UName, Phone_num, User_type) VALUES ('"
                               + str(form.cleaned_data['id']) + "', '" + str(encrypt_pw) + "', "
                               + "False" + ", '" + str(form.cleaned_data['uname']) + "', '" + str(phone_num)
                               + "', " +  "'f'" + ")")
                cursor.execute("INSERT INTO FREELANCERS (Id, Age, Exp, Major) VALUES ('"
                               + str(form.cleaned_data['id']) + "', '" + str(form.cleaned_data['age'])
                               + "', '" + str(form.cleaned_data['exp']) + "', '" + str(form.cleaned_data['major']) + "')")
                rows = cursor.fetchall()
                for i in range(len(langName)):
                    cursor.execute("INSERT INTO F_PROFICIENCY (Language, Star_rating, Fid) VALUES ('"
                                   + str(langName[i]) + "', '" + str(rating[i]) + "', '" + str(
                        form.cleaned_data['id']) + "')")
            return redirect('/registration/register_success')
    else:
        form = FreelancerForm()
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
                    cursor.execute("SELECT USER_TYPE FROM USERS WHERE ID='" + form.cleaned_data['id'] + "'")
                    rows = cursor.fetchone()
                    user_type = rows[0]
                    request.session['login'] = True
                    request.session['id'] = id
                    request.session['user_type'] = user_type
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
    del request.session['user_type']
    return render(request, 'registration/logout.html', {})

def make_request(request):
    context = {"make_request": "active"}
    if request.method == "POST":
        form = MakeRequestForm(request.POST)
        if form.is_valid():
            #reqtitle, fund, min_exp, min_fre, max_fre
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM REQUEST")
                rows = cursor.fetchone()
                req_id = rows[0]
                team_only = 0
                cid = request.session['id']
                if form.cleaned_data['min_fre'] >= 2:
                    team_only = 1
                cursor.execute("INSERT INTO REQUEST (Req_title, Req_id, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Team_only, State, Cid) VALUES ('"
                               + str(form.cleaned_data['reqtitle']) + "', '" + str(req_id) + "', '" + str(form.cleaned_data['fund']) + "', '"
                               + str(form.cleaned_data['min_exp']) + "', '" + str(form.cleaned_data['min_fre']) + "', '"
                               + str(form.cleaned_data['max_fre']) + "', '" + str(form.cleaned_data['start_date']) + "', '"
                               + str(form.cleaned_data['end_date']) + "', '" + str(team_only) + "', '0', '" + str(cid) + "')")
                rows = cursor.fetchall()
            return redirect('/request/request_success')
    else:
        form = MakeRequestForm()
    return render(request, 'request/make_request.html', {'form': form}, context)

def request_success(request):
    return render(request, 'request/request_success.html', {})

def mypage(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Rating from USERS WHERE Id = '" + str(request.session['id']) + "'")
        rating = cursor.fetchall()
        print(rating[0][0])
        if (rating[0][0] == None):
            rating = 'None'
        else:
            rating = str(rating).split('\'')
            rating = rating[1]
        cursor.execute("SELECT UName, Phone_num from USERS WHERE Id = '" + str(request.session['id']) + "'")
        info = cursor.fetchall()
    return render(request, 'mypage/mypage.html', {'rating': rating, 'info': info})

def update_client(request):
    if request.method == "POST":
        form = updateClientForm(request.POST)
        if form.is_valid():
            # id = request.session['id']
            # pw, uname, phone_num_0~2
            with connection.cursor() as cursor:
                encrypt_pw = base64.b64encode(hashlib.sha256(form.cleaned_data['pw'].encode()).digest()).decode()
                phone_num = form.cleaned_data['phone_num_0'] + form.cleaned_data['phone_num_1'] + form.cleaned_data['phone_num_2']
                cursor.execute("UPDATE USERS SET Pw = '" + str(encrypt_pw) + "', UName = '" + str(form.cleaned_data['uname']
                               + "', Phone_num = '" + str(phone_num)) + "' WHERE Id = '" + request.session['id'] + "'")
                rows = cursor.fetchall()
            return redirect('/mypage/mypage')
    else:
        form = updateClientForm()
        with connection.cursor() as cursor:
            cursor.execute("SELECT UName, Phone_num from USERS WHERE Id = '" + str(request.session['id']) + "'")
            info = cursor.fetchall()
    return render(request, 'mypage/update_client.html', {'form': form, 'info': info})

def update_freelancer(request):
    return render(request, 'mypage/update_freelancer.html', {})

def id_dup_check(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'USER_ID' in request.POST:
            uid = request.POST['USER_ID']
            cursor.execute("SELECT PW FROM USERS WHERE ID='" + uid + "'")
            rows = cursor.fetchone()
            if rows is None:
                return HttpResponse("False")
            else:
                return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def show_request(request):
    with connection.cursor() as cursor:
        cursor.execute("Select Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date from Request")
        rows = cursor.fetchall()
        print(rows)
    context = {"show_request": "active"}
    return render(request, 'request/show_request.html', {'myRequest': rows}, context)

def request_accept(request):
    return render(request, 'request/request_accept.html', {})