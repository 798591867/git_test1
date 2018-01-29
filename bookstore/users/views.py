from django.shortcuts import render, redirect
import re
from .models import Passport, Address
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from utils.decorators import login_required
from order.models import OrderInfo, OrderBooks
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from users.tasks import send_active_email
# Create your views here.


def register(request):

    return render(request, 'users/register.html')


def register_handle(request):
    """对用户的注册信息进行处理"""
    # TODO 接收数据
    username = request.POST.get('user_name', '')
    password = request.POST.get('pwd', '')
    email = request.POST.get('email', '')
    # 不能用中文注册
    if not re.match(r'^[a-zA-Z0-9_-]{4,16}$', username):
        return render(request, 'users/register.html', {'errmsg': '用户名只能包含大小写字母数下划线以及-号!'})
    # TODO 进行数据校验
    if not all([username, password, email]):
        # 如果数据有空
        return render(request, 'users/register.html', {'errmsg': '输入的信息不能为空,请核对后再重新输入!'})
    # TODO 验证邮箱地址
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'users/register.html', {'errmsg': '邮箱格式输入有误,请重新输入!'})
    # TODO 验证通过　将注册信息添加到数据库

    p = Passport.objects.filter(username=username)

    if p:
        return render(request, 'users/register.html', {'errmsg':'用户名已经存在'})
    passport = Passport.objects.add_one_passport(username=username, password=password, email=email)
    # 记住登录状态
    request.session['islogin'] = True
    request.session['username'] = username
    request.session['passport_id'] = passport.id
    # 生成激活的token itsdeangerous
    serializer = Serializer(settings.SECRET_KEY, 3600)
    token = serializer.dumps({'confirm':passport.id})
    token = token.decode('utf8')
    # 给用户的邮箱发送激活邮件
    # send_mail('书城用户激活','', settings.EMAIL_FROM, [email],html_message='<a href="http://192.168.28.66:8000/user/active/%s/">http://192.168.28.66:8000/user/active/</a>' % token)
    send_active_email.delay(token, username, email)
    return redirect(reverse('book:book_index'))



# todo 显示登录界面
def login(request):
    """显示登录界面"""
    username = request.COOKIES.get('username', '')
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

@login_required
def user(request):
    """用户中心-信息页"""
    passport_id = request.session.get('passport_id')
    # 获取用户的基本信息
    addr = Address.objects.get_default_address(passport_id=passport_id)


    books_li = []

    context = {
        'addr':addr,
        'page':'user',
        'books_li': books_li,
    }

    return render(request, 'users/user_center_info.html', context)



@login_required
def order(request):
    # 用户中心订单页
    # 查询用户的订单信息
    passport_id = request.session.get('passport_id')

    # 获取订单信息
    order_li = OrderInfo.objects.filter(passport_id=passport_id)


    # 便利获取订单的商品信息
    # order->OrderInfo 实例对象
    for order in order_li:
        # 根据订单的ID查询订单商品信息
        order_id = order.order_id
        order_books_li = OrderBooks.objects.filter(order_id=order_id)


        # 计算商品的小计
        # order_books->OrderBooks实例对象
        for order_books in order_books_li:
            count = order_books.count
            price = order_books.price
            amount = count * price
            # 保存订单中每一个商品的小计
            order_books.amount = amount

        # 给order对象动态增加一个属性order_books_li,保存订单中商品的信息
        order.order_books_li = order_books_li

    context = {
        'order_li':order_li,
        'page':'order'
    }

    return render(request, 'users/user_center_order.html', context)



@login_required
def address(request):
    # 用户中心地址页
    # 获取登录用户的id
    passport_id = request.session.get('passport_id')

    if request.method == 'GET':
        # 显示地址页面
        # 查询用户的默认地址
        addr = Address.objects.get_default_address(passport_id=passport_id)
        return render(request, 'users/user_center_site.html', {'addr':addr, 'page':'address'})
    else:
        # 添加收货地址
        # 1. 接受数据
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        recipient_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')

        # 2. 进行校验
        if not all ([recipient_addr, recipient_name, recipient_phone, zip_code]):
            return render(request, 'users/user_center_site.html', {'errmsg':'信息不能为空'})

        # 3.添加收货地址
        Address.objects.add_one_address(
            passport_id=passport_id,
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            recipient_addr=recipient_addr,
            zip_code=zip_code,
        )

        # 4.返回应答
        return redirect(reverse('user:address'))