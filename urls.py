from django.conf.urls import url
from . import views

app_name = 'headhunt'

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^registration/login/$', views.login, name = 'login'),
    url(r'^registration/logged_out/$', views.logout, name = 'logout'),
    url(r'^registration/register/$', views.register, name = 'register'),
    url(r'^registration/register_success/$', views.register_success, name = 'register_success'),
    #url(r'^$', views.IndexView.as_view(), name = 'index'),
    # /headhunt 로 접속시 (include 됨)
    # CBV의 generic view를 이용하여 url을 처리하겠다는 말
]