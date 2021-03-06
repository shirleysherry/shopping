from django.conf.urls import url

from todo.views import index, login, reg, forgetpassword, member, infor, msg_phone

urlpatterns = [
    url(r'^$', index, name='首页'),
    url(r'^login/$', login, name='登录'),
    url(r'^reg/$', reg, name='注册'),
    url(r'^forget/$', forgetpassword, name='忘记密码'),
    url(r'^member/$', member, name='个人中心'),
    url(r'^infor/$',infor, name='个人资料'),
    url(r'^sendMsg/$', msg_phone, name="短信地址"),
]
