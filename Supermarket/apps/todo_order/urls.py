from django.conf.urls import url

from todo.views import index, login, reg

urlpatterns = [
    url(r'^$',index,name='首页'),
    url(r'^login/$',login,name='登录'),
    url(r'^reg/$',reg,name='注册'),
    # url(r'^$',index,name='首页'),


]