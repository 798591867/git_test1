from django.shortcuts import render, redirect
import re
from .models import Passport
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse


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
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'users/register.html', {'errmsg': '邮箱格式输入有误,请重新输入!'})
    # TODO 验证通过　将注册信息添加到数据库

    passport = Passport.objects.add_one_passport(username=username, password=password, email=email)

    return redirect(reverse('book:book_index'))


# todo 显示登录界面
def login(request):
    """显示登录界面"""
    username = ''
    checked = ''
    context = {
        'username': username,
        'checked': checked,
    }
    return render(request, 'users/login.html', context)


# todo 登录数据的校验功能,还有记住用户名的功能
def login_check(request):
    # 1.获取数据
    username = request.POST['username']
    password = request.POST['password']
    remember = request.POST['remember']
    # 2.数据校验
    if not all([username, password, remember]):
        # 有数据为空
        return JsonResponse({'res': 2})
    # 3.进行处理:根据用户名和密码查找用户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    if passport:
        # 用户名密码正确
        # 获取session中的url_path
        # if request.session.has_key('url_path')
        #   next_url = request.session.get('url_path')
        # else:
        #   next_url = reverse('book:index')
        next_url = request.session.get('url_path', reverse('book:book_index'))
        jres = JsonResponse({'res': 1, 'next_url': next_url})

        # 判断是否需要记住用户名
        if remember == 'true':
            # 记住用户名
            jres.set_cookie('username', username, max_age=7 * 24 * 3600)
        else:
            # 不记住用户名
            jres.delete_cookie('username')
        # 记住用户的登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id
        return jres
    else:
        # 用户名或密码错误
        return JsonResponse({'res': 0})


def logout(request):
    """用户退出登录"""
    # 清空用户的session信息
    request.session.flush()
    # 跳转到首页
    return redirect(reverse('book:book_index'))
