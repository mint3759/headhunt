from django.shortcuts import render, redirect
from .models import Users
from .forms import *
from django.forms.utils import ErrorList
from django.db import connection
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
import base64
import hashlib
import decimal

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
        print(request.POST)
        if form.is_valid():
            #reqtitle, fund, min_exp, min_fre, max_fre
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
                cursor.execute("SELECT MAX(req_id) FROM REQUEST")
                rows = cursor.fetchone()
                if rows[0] is None:
                    req_id = 1
                else:
                    req_id = rows[0] + 1
                team_only = 0
                cid = request.session['id']
                if form.cleaned_data['min_fre'] >= 2:
                    team_only = 1
                cursor.execute("INSERT INTO REQUEST (Req_title, Req_id, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Team_only, State, Cid) VALUES ('"
                               + str(form.cleaned_data['reqtitle']) + "', '" + str(req_id) + "', '" + str(form.cleaned_data['fund']) + "', '"
                               + str(form.cleaned_data['min_exp']) + "', '" + str(form.cleaned_data['min_fre']) + "', '"
                               + str(form.cleaned_data['max_fre']) + "', '" + str(form.cleaned_data['start_date']) + "', '"
                               + str(form.cleaned_data['end_date']) + "', '" + str(team_only) + "', '0', '" + str(cid) + "')")
                for i in range(len(langName)):
                    cursor.execute("INSERT INTO R_PROFICIENCY (Language, Star_rating, Req_id) VALUES ('"
                                   + str(langName[i]) + "', '" + str(rating[i]) + "', '" + str(
                        req_id) + "')")
            return redirect('/request/request_success')
    else:
        form = MakeRequestForm()
    return render(request, 'request/make_request.html', {'form': form}, context)

def request_success(request):
    return render(request, 'request/request_success.html', {})

def remove_myrequest(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            rid = request.POST['REQ_ID']
            cursor.execute("DELETE FROM REQUEST WHERE Req_id='" + rid + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

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

def myrequest_client(request):
    #구인대기중인
    with connection.cursor() as cursor:
        cursor.execute("Select * from Request where Cid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        myRequest = []
        for i in range(len(rows)):
            if rows[i] == None:
                'Error. Not existed request'
            else:
                cursor.execute("Select * from Request where Req_id = '" + str(rows[i][0]) + "' AND STATE=0")
                tmp_myRequest = cursor.fetchall()
                for j in range(len(tmp_myRequest)):
                    myRequest.append((tmp_myRequest[j], 'X'))
                    print("my Request")
                    print(myRequest)

    #수락 요청중인
        cursor.execute("Select * from Request where Cid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        AnswerForRequest = []
        for i in range(len(rows)):
            cursor.execute("Select * from Request where Req_id = '" + str(rows[i][0]) + "'AND STATE=1")
            tmp_AnswerForRequest = cursor.fetchall()
            for j in range(len(tmp_AnswerForRequest)):
                AnswerForRequest.append((tmp_AnswerForRequest[j], 'X'))
                print("answer for request")
                print(AnswerForRequest)
    #진행중인
        cursor.execute("Select * from Request where Cid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        WorkingRequest = []
        for i in range(len(rows)):
            cursor.execute("Select * from Request where Req_id = '" + str(rows[i][0]) + "'AND STATE=2")
            tmp_WorkingRequest = cursor.fetchall()
            for j in range(len(tmp_WorkingRequest)):
                WorkingRequest.append((tmp_WorkingRequest[j], 'X'))
                print("working Request")
                print(WorkingRequest)
    #완료 요청
        cursor.execute("Select * from Request where Cid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        CompletedRequestW = []
        for i in range(len(rows)):
            cursor.execute("Select * from Request where Req_id = '" + str(rows[i][0]) + "'AND STATE=3")
            tmp_CompletedRequestW = cursor.fetchall()
            for j in range(len(tmp_CompletedRequestW)):
                CompletedRequestW.append((tmp_CompletedRequestW[j], 'X'))
                print("Completed W Request")
                print(CompletedRequestW)
    #완료
        cursor.execute("Select * from Request where Cid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        CompletedRequest = []
        for i in range(len(rows)):
            cursor.execute("Select * from Request where Req_id = '" + str(rows[i][0]) + "'AND STATE=4")
            tmp_CompletedRequest = cursor.fetchall()
            for j in range(len(tmp_CompletedRequest)):
                CompletedRequest.append((tmp_CompletedRequest[j], 'X'))
                print("Completet Request")
                print(CompletedRequest)
    return render(request, 'mypage/myrequest_client.html', {'myRequest': myRequest,
                                                            'AnswerForRequest': AnswerForRequest,
                                                            'WorkingRequest': WorkingRequest,
                                                            'CompletedRequestW': CompletedRequestW,
                                                            'CompletedRequest': CompletedRequest})

def remove_myrequest_client(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            rid = request.POST['REQ_ID']
            cursor.execute("DELETE FROM REQUEST WHERE Req_id='" + rid + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def cl_acc_request(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            req_id = request.POST['REQ_ID']
            cursor.execute("UPDATE REQUEST SET State = 2 WHERE Req_id = '" + req_id + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def accept_req_fromfree(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            req_id = request.POST['REQ_ID']
            cursor.execute("UPDATE REQUEST SET State = 4 WHERE Req_id = '" + req_id + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def update_freerating(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST and 'Frating' in request.POST:
            req_id = request.POST['REQ_ID']
            cursor.execute("UPDATE REQUEST SET State = 4 WHERE Req_id = '" + req_id + "'")
            Frating = request.POST['Frating']
            cursor.execute("UPDATE REQUEST SET Frating = '" + Frating + "' WHERE Req_id = '" + str(req_id) + "'")
            cursor.execute("SELECT Cid FROM CONTRACTS WHERE Rid = '" + str(req_id) + "'")
            rows = cursor.fetchall()
            cid = rows[0][0]
            cursor.execute("SELECT Frating FROM REQUEST WHERE Cid = '" + cid + "' AND State = 4")
            rows = cursor.fetchall()
            rating = rows[0][0]
            for i in range(len(rows)):
                if i == 0:
                    continue
                rating = rating + rows[i][0]
            average = rating / decimal.Decimal(len(rows))
            cursor.execute("UPDATE USERS SET Rating = '" + str(average) + "' WHERE Id = '" + cid + "'")
            return HttpResponse("True")

def show_freelancer(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("Select * from Request_ask WHERE Rid = '" + pk + "'")
        rows = cursor.fetchall()
        print(rows)
        # rows[i][1] is fid
        freeInfo = []
        for i in range(len(rows)):
            cursor.execute("Select * from Freelancers WHERE Id = '" + rows[i][1] + "'")
            r = cursor.fetchall()
            freeInfo.append(r[0])
        print(freeInfo)
        # freeInfo[0][0] is fid
        users = []
        for i in range(len(rows)):
            cursor.execute("Select * from Users WHERE Id = '" + freeInfo[i][0] + "'")
            r = cursor.fetchall()
            users.append(r[0])
        print(users)
        print(rows)
        info = []
        for i in range(len(users)):
            info.append((freeInfo[i], users[i]))
        print(info)
        print(info[0][0])
    context = {"show_freelancer": "active"}
    return render(request, 'mypage/show_freelancer.html', {'info': info}, context)


def select_requestAsk_client(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            req_id = request.POST['REQ_ID']
            cursor.execute("UPDATE REQUEST SET State = 2 WHERE Req_id = '" + req_id + "'")
            cursor.execute("DELETE from REQUEST_ASK WHERE Rid = '" + req_id + "'")
            # cursor.execute("INSERT CONTRACTS (Rid, Cid, Fid) VALUES ('" + req_id + "', '" + request.session['id'] + "', '" + freelancer1')")

            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def myrequest_freelancer(request):
    with connection.cursor() as cursor:
        #수락 요청 중인 의뢰
        #개인
        cursor.execute("SELECT Rid FROM REQUEST_ASK WHERE Fid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        #rows[i][0]은 해당하는 request의 req_id
        myRequestAsk = []
        for i in range(len(rows)):
            cursor.execute("SELECT Req_id, Req_title, fund, Start_date, End_date, Min_exp, Min_fre, Max_fre, Team_only, State, Frating, Crating, Cid " +
                            "FROM REQUEST WHERE Req_id = '" + str(rows[i][0]) + "'")
            tmp_myRequestAsk = cursor.fetchall()
            for j in range(len(tmp_myRequestAsk)):
                myRequestAsk.append((tmp_myRequestAsk[j], 'X'))
        print(myRequestAsk)
        #팀
        cursor.execute("SELECT Tname FROM TEAMS WHERE Leader = '" + request.session['id'] + "'")
        teams = cursor.fetchall()
        print(teams)
        for i in range(len(teams)):
            tName = teams[i][0]
            cursor.execute("SELECT Rid FROM REQUEST_TEAM_ASK WHERE Tname = '" + tName + "'")
            rows = cursor.fetchall()
            # rows[i][0]은 해당하는 request의 req_id
            for j in range(len(rows)):
                cursor.execute("SELECT Req_id, Req_title, fund, Start_date, End_date, Min_exp, Min_fre, Max_fre, Team_only, State, Frating, Crating, Cid " +
                            "FROM REQUEST WHERE Req_id = '" + str(rows[i][0]) + "'")
                tmp_myRequestAsk = cursor.fetchall()
                for k in range(len(tmp_myRequestAsk)):
                    myRequestAsk.append((tmp_myRequestAsk[k], 'O', tName))
        print(myRequestAsk)

        #진행 중인 의뢰
        #개인
        cursor.execute("SELECT Rid FROM CONTRACTS WHERE Fid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        #rows[i][0]는 원하는 req_id
        myWorkingRequest = []
        msgCheck = []
        message = []
        for i in range(len(rows)):
            cursor.execute("SELECT Req_id, Req_title, fund, Start_date, End_date, Min_exp, Min_fre, Max_fre, Team_only, State, Frating, Crating, Cid " +
                            "FROM REQUEST WHERE Req_id = '" + str(rows[i][0]) + "' AND STATE = 2")
            tmp_myWorkingRequest = cursor.fetchall()
            cursor.execute("SELECT Message FROM MESSAGE WHERE Rid = '" + str(rows[i][0]) + "'")
            tmpMsg = cursor.fetchall()
            if not tmpMsg:
                msgCheck.append('None')
                message.append('None')
            else:
                msgCheck.append('True')
                message.append(tmpMsg[0][0])
            for j in range(len(tmp_myWorkingRequest)):
                if not tmpMsg:
                    myWorkingRequest.append((tmp_myWorkingRequest[j], 'X', 'None', 'None'))
                else:
                    myWorkingRequest.append((tmp_myWorkingRequest[j], 'X', 'Yes', tmpMsg[0][0]))
        print(myWorkingRequest)

        #완료 요청 중인 의뢰
        #개인
        cursor.execute("SELECT Rid FROM CONTRACTS WHERE Fid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        # rows[i][0]는 원하는 req_id
        myCompleteAsk = []
        for i in range(len(rows)):
            cursor.execute("SELECT Req_id, Req_title, fund, Start_date, End_date, Min_exp, Min_fre, Max_fre, Team_only, State, Frating, Crating, Cid " +
                            "FROM REQUEST WHERE Req_id = '" + str(rows[i][0]) + "' AND STATE = 3")
            tmp_myCompleteAsk = cursor.fetchall()
            for j in range(len(tmp_myCompleteAsk)):
                myCompleteAsk.append((tmp_myCompleteAsk[j], 'X'))
        print(myCompleteAsk)

        #완료된 의뢰
        #개인
        cursor.execute("SELECT Rid FROM CONTRACTS WHERE Fid = '" + request.session['id'] + "'")
        rows = cursor.fetchall()
        # rows[i][0]는 원하는 req_id
        myCompleteRequest = []
        for i in range(len(rows)):
            cursor.execute("SELECT Req_id, Req_title, fund, Start_date, End_date, Min_exp, Min_fre, Max_fre, Team_only, State, Frating, Crating, Cid " +
                            "FROM REQUEST WHERE Req_id = '" + str(rows[i][0]) + "' AND STATE = 4")
            tmp_myCompleteRequest = cursor.fetchall()
            for j in range(len(tmp_myCompleteRequest)):
                if tmp_myCompleteRequest[j][11] is None:
                    myCompleteRequest.append((tmp_myCompleteRequest[j], 'X', 'X'))
                else:
                    myCompleteRequest.append((tmp_myCompleteRequest[j], 'X', 'O'))
    return render(request, 'mypage/myrequest_freelancer.html', {'myRequestAsk': myRequestAsk,
                                                                'myWorkingRequest': myWorkingRequest,
                                                                'myCompleteAsk': myCompleteAsk,
                                                                'myCompleteRequest': myCompleteRequest,
                                                                'msgCheck': msgCheck,
                                                                'message': message})

def remove_requestAsk_freelancer(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            req_id = request.POST['REQ_ID']
            cursor.execute("UPDATE REQUEST SET State = 0 WHERE Req_id = '" + req_id + "'")
            cursor.execute("DELETE from REQUEST_ASK WHERE Rid = '" + req_id + "' AND Fid = '" + request.session['id'] + "'")
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def askComplete(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            req_id = request.POST['REQ_ID']
            cursor.execute("UPDATE REQUEST SET State = 3 WHERE Req_id = '" + req_id + "'")
            #파일첨부해야함
            return HttpResponse("True")
        else:
            return HttpResponse("Fail")

def update_Crating(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST and 'Crating' in request.POST:
            req_id = request.POST['REQ_ID']
            Crating = request.POST['Crating']

            #평가하기
            cursor.execute("UPDATE REQUEST SET Crating = '" + Crating + "' WHERE Req_id = '" + str(req_id) + "'")

            #클라이언트 평점 업데이트
            cursor.execute("SELECT Cid FROM CONTRACTS WHERE Rid = '" + str(req_id) + "'")
            rows = cursor.fetchall()
            cid = rows[0][0]
            cursor.execute("SELECT Crating FROM REQUEST WHERE Cid = '" + cid + "' AND State = 4")
            rows = cursor.fetchall()
            rating = rows[0][0]
            for i in range(len(rows)):
                if i == 0:
                    continue
                rating = rating + rows[i][0]
            average = rating / decimal.Decimal(len(rows))
            cursor.execute("UPDATE USERS SET Rating = '" + str(average) + "' WHERE Id = '" + cid + "'")

            #내부 포트폴리오 추가
            cursor.execute("SELECT MAX(req_id) FROM PORTFOLIO")
            rows = cursor.fetchone()
            print(rows)
            if rows[0] is None:
                port_id = 1
            else:
                port_id = rows[0] + 1
            cursor.execute("INSERT PORTFOLIO (Id, Fid, Class, Req_id) VALUES ('" + str(port_id) + "', '" + request.session['id'] + "', 'I', '" + req_id + "')")
            return HttpResponse("True")
        
def myportfolio(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PortFolio WHERE Class = 'I' AND Fid = '" + request.session['id'] + "'")
        tmpPortI = cursor.fetchall()
        print(tmpPortI)
        portI = []
        for i in range(len(tmpPortI)):
            cursor.execute("SELECT * FROM REQUEST WHERE Req_id = '" + str(tmpPortI[i][5]) + "'")
            rows = cursor.fetchall()
            print(rows)
            portI.append((rows[0], tmpPortI[i]))
        print(portI)
        cursor.execute("SELECT * FROM PortFolio WHERE Class = 'E' AND Fid = '" + request.session['id'] + "'")
        tmpPortE = cursor.fetchall()
        portE = []
        print(portE)
    return render(request, 'mypage/myportfolio.html', {'portI': portI, 'portE': portE})

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

def member_check(request):
    with connection.cursor() as cursor:
        print(request.POST)
        if 'USER_ID' in request.POST and 'TEAM_ID' in request.POST:
            uid = request.POST['USER_ID']
            tid = request.POST['TEAM_ID']
            cursor.execute("SELECT * FROM USERS WHERE ID='" + uid + "' AND USER_TYPE='f'")
            rows = cursor.fetchone()
            if rows is None:
                return HttpResponse("no_id")
            else:
                cursor.execute("SELECT * FROM PARTICIPATE_IN WHERE Tname = '" + tid + "' AND Fid='" + uid + "'")
                rows = cursor.fetchone()
                if rows is not None:
                    return HttpResponse("exist_member")
                cursor.execute("INSERT INTO PARTICIPATE_IN (Tname, Fid) VALUES ('" + tid + "', '" + uid + "')")
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

def show_request(request, pk):
    with connection.cursor() as cursor:
        if pk == '1':  # 날짜순 정렬 DESC
            print(pk + ': 1')
            cursor.execute(
                "Select Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id from Request WHERE state=0 ORDER BY Start_date DESC")
        elif pk == '2':  # 날짜순 정렬 ASC
            print(pk + ': 2')
            cursor.execute(
                "Select Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id from Request WHERE state=0 ORDER BY Start_date ASC")
        elif pk == '3':  # 금액순 정렬 DESC
            print(pk + ': 3')
            cursor.execute(
                "Select Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id from Request WHERE state=0 ORDER BY FUND DESC")
        elif pk == '4':  # 금액순 정렬 ASC
            print(pk + ': 4')
            cursor.execute(
                "Select Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id from Request WHERE state=0 ORDER BY FUND ASC")
        else:  # 기본 보여주기
            print(pk + ': 0')
            cursor.execute("Select Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id from Request WHERE state=0")
        rows = cursor.fetchall()
    context = {"show_request": "active"}
    return render(request, 'request/show_request.html', {'myRequest': rows, 'pk': pk}, context)

def request_accept(request):
    return render(request, 'request/request_accept.html', {})

def request_content(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("Select * from Request where Req_id = '" + pk + "'")
        rows = cursor.fetchall()
        cursor.execute("Select Language, Star_rating from R_PROFICIENCY WHERE req_id = '" + pk + "'")
        rows2 = cursor.fetchall()
        #Req_title, Fund, Min_exp, Min_fre, Max_fre, Start_date, End_date, Crating, Req_id
    context = {"request_content": "active"}
    return render(request, 'request/request_content.html', {'req': rows[0], 'proficiency': rows2}, context)

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


def check_accept_req(request):
    with connection.cursor() as cursor:
        if 'REQ_ID' in request.POST:
            rid = request.POST['REQ_ID']
            fid = request.POST['F_ID']
            cursor.execute("SELECT * from R_PROFICIENCY where req_id='" + rid + "' and EXISTS (SELECT * from REQUEST WHERE Request.req_id=R_proficiency.req_id)")
            req_rows=cursor.fetchall()
            if not req_rows: #제약조건이 없는 경우
                string = "INSERT INTO REQUEST_ASK (Rid, Fid) VALUES ('" + rid + "','" + fid + "');"
                print(string)
                cursor.execute("INSERT INTO REQUEST_ASK (Rid, Fid) VALUES ('" + rid + "','" + fid + "')")
                cursor.execute("UPDATE REQUEST SET State=1 WHERE Req_id=" +rid + "")
                return HttpResponse("True")
            else:
                cursor.execute("SELECT * from F_PROFICIENCY WHERE fid = '" + fid + "'")
                fre_rows = cursor.fetchall()
                if fre_rows is None:
                    return HttpResponse("False")
                for rr in req_rows:
                    is_found = False
                    for fr in fre_rows:
                        if rr[0] == fr[0]:
                            if rr[1] <= fr[1]:
                                is_found = True
                                break
                            else:
                                return HttpResponse("False")
                    if is_found is False:
                        return HttpResponse("False")
                cursor.execute("INSERT INTO REQUEST_ASK (Rid, Fid) VALUES ('" + rid + "','" + fid + "')")
                cursor.execute("UPDATE REQUEST SET State=1 WHERE Req_id=" + rid + "")
                return HttpResponse("True")
        else:
            return HttpResponse("Fail")