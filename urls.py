from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'headhunt'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^registration/login/$', auth_views.LoginView.as_view, name = 'login'),
    url(r'^registration/logout/$', views.logout, name = 'logout'),
    url(r'^registration/register/$', views.register, name = 'register'),
    url(r'^registration/id_dup_check/$', views.id_dup_check, name = 'id_dup_check'),
    url(r'^registration/register_client/$', views.register_client, name = 'register_client'),
    url(r'^registration/register_freelancer/$', views.register_freelancer, name = 'register_freelancer'),
    url(r'^registration/register_portfolio/$', views.register_portfolio, name='register_portfolio'),
    url(r'^registration/register_success/$', views.register_success, name = 'register_success'),
    url(r'^request/request_success/$', views.request_success, name = 'request_success'),
    url(r'^request/make_request/$', views.make_request, name = 'make_request'),
    url(r'^mypage/mypage/$', views.mypage, name = 'mypage'),
    url(r'^mypage/myportfolio/$', views.myportfolio, name='myportfolio'),
    url(r'^mypage/myteam/$', views.myteam, name='myteam'),
    url(r'^mypage/id_free_check/$', views.id_free_check, name='id_free_check'),
    url(r'^mypage/tName_check/$', views.tName_check, name='tName_check'),
    url(r'^mypage/update_client/$', views.update_client, name = 'update_client'),
    url(r'^mypage/update_freelancer/$', views.update_freelancer, name = 'update_freelancer'),
    url(r'^request/show_request/$', views.show_request, name = 'show_request'),
    url(r'^request/request_accept/$', views.request_accept, name = 'request_accept'),
    url(r'^request/request_content/(?P<pk>\d+)/$', views.request_content, name = 'request_content'),
    url(r'^administrator/admin_account/$', views.admin_account, name = 'admin_account'),
    url(r'^administrator/admin_req/$', views.admin_req, name = 'admin_req'),
    url(r'^administrator/admin_team/$', views.admin_team, name = 'admin_team'),
    url(r'^administrator/remove_account/$', views.remove_account, name = 'remove_account'),
    #url(r'^$', views.IndexView.as_view(), name = 'index'),url(r'^request/show_request/$', views.show_request, name='show_request'),
    # /headhunt 로 접속시 (include 됨)
    # CBV의 generic view를 이용하여 url을 처리하겠다는 말
]