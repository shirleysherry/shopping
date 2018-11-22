import hashlib
import random
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from todo.forms import RegForm, LoginForm
from todo.helper import set_password, my_login, verify_login, send_sms
from todo.models import User
import re
from django_redis import get_redis_connection


@verify_login
def index(request):
    return render(request, 'todo/index.html')


def login(request):  # 登录
    # 接收数据
    if request.method == "POST":
        data = request.POST
        # 验证数据
        lo_form = LoginForm(data)
        if lo_form.is_valid():
            # 将登陆标识放到session中
            user1 = lo_form.cleaned_data.get('telephone')
            #  在数据库中查找手机号的id
            user1 = User.objects.get(telephone=data.get("telephone"))
            my_login(request, user1)
            return redirect('todo:个人中心')
        else:
            context = {
                "errors": lo_form.errors,
            }
            return render(request, "todo/login.html", context)
    else:

        return render(request, "todo/login.html")


def reg(request):
    # 接收
    data = request.POST
    # 验证数据
    form = RegForm(data)
    if form.is_valid():
        # 处理
        data = form.cleaned_data
        # 加密
        password = data.get('password2')
        password = set_password(password)
        # 保存到数据库
        User.objects.create(telephone=data.get('telephone'), password=password)

        return redirect("todo:登录")
    else:
        # 错误信息
        context = {
            "errors": form.errors,
        }
        return render(request, "todo/reg.html", context)


@verify_login
def forgetpassword(request):
    return render(request, 'todo/forgetpassword.html')


@verify_login
def member(request):
    return render(request, 'todo/member.html')


@verify_login
def infor(request):
    return render(request, 'todo/infor.html')


def msg_phone(request):
    if request.method == 'POST':
        # 接收手机号并验证
        telephone = request.POST.get("telephone,")
        # 创建正则
        rr = re.compile("^1[3-9]\d{9}$")
        rs = re.search(rr,telephone)
        if rs is None:
            return JsonResponse({"err": 1, "errmsg": "手机格式错误"})
        # 生成随机码
        random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])

        # 保存到redis
        w = get_redis_connection("default")
        w.set(telephone, random_code)
        # 设置过期时间
        w.expire(telephone, 120)
        print(random_code)

        #  使用阿里发生短信
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"网上超市\"}" % random_code
        send_sms(__business_id, telephone, "注册验证", "SMS_2245271", params)

        return JsonResponse({"err": random_code})

    else:

        return JsonResponse({"err":1,"errmsg":"请求方式错误"})