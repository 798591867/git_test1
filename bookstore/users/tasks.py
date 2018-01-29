from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_active_email(token,username, email):
    # 发送激活邮件
    subject = '书城用户激活'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [email]
    html_message = '<a href="http://192.168.28.66:8000/user/active/%s/">http://192.168.28.66:8000/user/active/</a>'%token
    send_mail(subject, message, sender, receiver,html_message=html_message)