from django.db import connection

def id_dup_check(request):
    with connection.cursor() as cursor:
        uid = request.POST['USER_ID']
        cursor.execute("SELECT PW FROM USERS WHERE ID='" + uid + "'")
        rows = cursor.fetchone()
        if rows is None:
            return False
        else:
            return True