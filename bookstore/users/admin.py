from django.contrib import admin
from .models import Passport, Address

# TODO 注册Passport 到数据库
admin.site.register(Passport)
admin.site.register(Address)
