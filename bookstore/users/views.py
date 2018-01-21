from django.shortcuts import render
import re
from .models import Passport

# Create your views here.


def register(request):
    return render(request, 'users/register.html')


def register_handle(request):
    """对用户的注册信息进行处理"""
    # TODO 接收数据
    username = request.POST.get('user_name', '')
    password = request.POST.get('pwd', '')
    email = request.POST.get('email', '')

    # TODO 进行数据校验
    if not all([username, password, email]):
        # 如果数据有空
        return render(request, 'users/register.html', {'errmsg': '输入的信息不能为空,请核对后再重新输入!'})
    # TODO 验证邮箱地址
    elif not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'users/register.html', {'errmsg': '邮箱格式输入有误,请重新输入!'})
    # TODO 验证通过　将注册信息添加到数据库
    else:
        passport = Passport.objects.add_one_passport(username=username, password=password, email=email)
    return render(request, 'users/register.html', {'errmsg': '注册成功!'})
