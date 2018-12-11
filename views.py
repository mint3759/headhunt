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
                cursor.execute("INSERT INTO USERS (Id, Pw, UName, Phone_num, User_type) VALUES ('"
                               + str(form.cleaned_data['id']) + "', '" + str(encrypt_pw) + "', '"
                               + str(form.cleaned_data['uname']) + "', '" + str(phone_num)
                               + "', " + "'c'" + ")")
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
        print(request.POST)
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
                cursor.execute("INSERT INTO USERS (Id, Pw, UName, Phone_num, User_type) VALUES ('"
                               + str(form.cleaned_data['id']) + "', '" + str(encrypt_pw) + "', '"
                               + str(form.cleaned_data['uname']) + "', '" + str(phone_num)
                               + "', " + "'f'" + ")")
                cursor.execute("INSERT INTO FREELANCERS (Id, Age, Exp, Major) VALUES ('"
                               + str(form.cleaned_data['id']) + "', '" + str(form.cleaned_data['age'])
                               + "', '" + str(form.cleaned_data['exp']) + "', '" + str(form.cleaned_data['major']) + "')")
                rows = cursor.fetchall()
                for i in range(len(langName)):
                    cursor.execute("INSERT INTO F_PROFICIENCY (Language, Star_rating, Fid) VALUES ('"
                                   + str(langName[i]) + "', '" + str(rating[i]) + "', '" + str(
                        form.cleaned_data['id']) + "')")
            return redirect('/registration/register_portfolio')
    else:
        form = FreelancerForm()
    return render(request, 'registration/register_freelancer.html', {'form': form})

def register_portfolio(request):
    return render(request, 'registration/register_portfolio.html', {})
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

def myportfolio(request):
    return render(request, 'mypage/myportfolio.html', {})

def myteam(request):
    if request.method == "POST":
        form = MakeTeamForm(request.POST)
        if form.is_valid():
            print(form)
            tmpIdList = form.cleaned_data['teammate'].split(",")
            teammates = []
            for tmpId in tmpIdList:
                print(tmpIdList)
                teammates.append(tmpId)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO TEAMS (Tname, Leader) VALUES ('" + form.cleaned_data['tName'] + "', '" + request.session['id'] + "')")
                for i in range(len(teammates)):
                    cursor.execute("INSERT INTO PARTICIPATE_IN (Tname, Fid) VALUES ('" + form.cleaned_data['tName'] + "', '" + teammates[i] + "')")
            return redirect('/mypage/myteam', {})
    else:
        form = MakeTeamForm()
        with connection.cursor() as cursor:
            # start of 내가 속한 팀 조회 코드
            cursor.execute("SELECT Tname FROM PARTICIPATE_IN WHERE Fid = '" + request.session['id'] + "'")
            myteams = cursor.fetchall()
            tmpTeamInfo = []
            for i in range(len(myteams)):
                cursor.execute("SELECT * FROM TEAMS WHERE Tname = '" + myteams[i][0] + "'")
                tmpTeamInfo.append(cursor.fetchone())
            tmpTeammates = []
            for i in range(len(tmpTeamInfo)):
                cursor.execute("SELECT * FROM PARTICIPATE_IN WHERE Tname = '" + tmpTeamInfo[i][0] + "'")
                tmpTeammates.append(cursor.fetchall())
            teamMates = []
            teamMateNr = []
            for i in range(len(tmpTeammates)):
                str = []
                tmpLen = len(tmpTeammates[i])
                for j in range(tmpLen):
                    str.append(tmpTeammates[i][j][1])
                teamMates.append(str)
                teamMateNr.append(tmpLen)
            teamInfo = []
            for i in range(len(myteams)):
                teamInfo.append((tmpTeamInfo[i][0], tmpTeamInfo[i][1], teamMateNr[i], teamMates[i]))
            print(teamInfo)
            # end of 내가 속한 팀 조회 코드

            # start of 내가 만든 팀 관리 코드
            cursor.execute("SELECT Tname FROM TEAMS WHERE LEADER = '" + request.session['id'] + "'")
            teamNames = cursor.fetchall()
            tmpTeammates2 = []
            for i in range(len(teamNames)):
                cursor.execute("SELECT Fid FROM PARTICIPATE_IN WHERE Tname = '" + teamNames[i][0] + "'")
                tmpTeammates2.append(cursor.fetchall())
            teamMateNr_L = []
            for i in range(len(teamNames)):
                teamMateNr_L.append(len(tmpTeammates2[i]))
            teamInfoLeader = []
            for i in range(len(teamNames)):
                teamInfoLeader.append((teamNames[i], teamMateNr_L[i], tmpTeammates2[i]))
            # end of 내가 만든 팀 관리 코드
        return render(request, 'mypage/myteam.html', {'form': form, 'teamInfo': teamInfo, 'teamInfoLeader': teamInfoLeader})

def myrequest(request):
    with connection.cursor() as cursor:
        cursor.execute("Select * from request")
        rows = cursor.fetchall()
    return render(request, 'mypage/myrequest.html', {'myrequest': rows})

def remove_myrequest(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            rid = request.POST['REQ_ID']
            cursor.execute("DELETE FROM REQUEST WHERE Req_id='" + rid + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def id_dup_check(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'USER_ID' in request.POST:
            uid = request.POST['USER_ID']
            cursor.execute("SELECT * FROM USERS WHERE ID='" + uid + "'")
            rows = cursor.fetchone()
            if rows is None:
                return HttpResponse("False")
            else:
                return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def id_free_check(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'USER_ID' in request.POST:
            uid = request.POST['USER_ID']
            cursor.execute("SELECT * FROM USERS WHERE ID='" + uid + "' AND USER_TYPE='f'")
            rows = cursor.fetchone()
            if rows is None:
                return HttpResponse("False")
            else:
                return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def tName_check(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'tName' in request.POST:
            tname = request.POST['tName']
            cursor.execute("SELECT * FROM TEAMS WHERE Tname='" + tname + "'")
            rows = cursor.fetchone()
            print(rows)
            if rows is None:
                return HttpResponse("True")
            else:
                return HttpResponse("False")
        else:
            return HttpResponse("Fail")

def remove_member(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'USER_ID' in request.POST:
            uid = request.POST['USER_ID'].split(',')
            cursor.execute("DELETE FROM PARTICIPATE_IN WHERE Tname = '" + uid[0] + "' AND Fid='" + uid[1] + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def remove_team(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'Tname' in request.POST:
            tname = request.POST['Tname']
            cursor.execute("DELETE FROM TEAMS WHERE Tname = '" + tname + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def show_request(request):
    with connection.cursor() as cursor:
        cursor.execute("Select Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id from Request")
        rows = cursor.fetchall()
        print(rows)
    context = {"show_request": "active"}
    return render(request, 'request/show_request.html', {'myRequest': rows}, context)

def request_accept(request):
    return render(request, 'request/request_accept.html', {})

def request_content(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("Select * from Request where Req_id = '" + pk + "'")
        rows = cursor.fetchall()
        print(rows)
        #Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id
    context = {"request_content": "active"}
    return render(request, 'request/request_content.html', {'req': rows[0]}, context)

def admin_account(request):
    with connection.cursor() as cursor:
        cursor.execute("Select * from users")
        rows = cursor.fetchall()
        print(rows)
    return render(request, 'administrator/admin_account.html', {'accounts': rows})

def remove_account(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'USER_ID' in request.POST:
            uid = request.POST['USER_ID']
            cursor.execute("DELETE FROM USERS WHERE ID='" + uid + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def admin_req(request):
    with connection.cursor() as cursor:
        cursor.execute("Select * from request")
        rows = cursor.fetchall()
        cursor.execute("SELECT * from Message")
        rows2 = cursor.fetchall()
    return render(request, 'administrator/admin_req.html', {'requests' : rows, 'rej_requests' : rows2}, )

def remove_request(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            rid = request.POST['REQ_ID']
            cursor.execute("DELETE FROM REQUEST WHERE Req_id='" + rid + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def remove_request_rej(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            rid = request.POST['REQ_ID']
            cursor.execute("DELETE FROM MESSAGE WHERE Rid='" + rid + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def admin_team(request):
    with connection.cursor() as cursor:
        cursor.execute("Select * from teams")
        rows = cursor.fetchall()
        cursor.execute("Select * from t_contracts")
        rows2 = cursor.fetchall()
    return render(request, 'administrator/admin_team.html', {'teams':rows})


def remove_team_admin(request):
    with connection.cursor() as cursor:
        if 'TEAM_NAME' in request.POST:
            tname = request.POST['TEAM_NAME']
            cursor.execute("DELETE FROM TEAMS WHERE Tname='" + tname + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")