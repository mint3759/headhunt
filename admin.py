from django.contrib import admin

# Register your models here.
from .models import Users, Freelancers, Clients, Request, Teams

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'pw', 'uname', 'phone_num', 'rating', 'user_type')

class ReqAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'state', 'fund', 'start_date', 'end_date', 'min_exp', 'min_fre', 'max_fre', 'team_only', 'frating', 'crating', 'cid')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('tname', 'leader')

# 클래스를 어드민 사이트에 등록
admin.site.register(Users, UserAdmin)
admin.site.register(Request, ReqAdmin)
admin.site.register(Teams, TeamAdmin)