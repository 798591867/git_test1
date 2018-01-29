from django.db import models
from db.base_model import BaseModel
from public.get_hash import get_hash


# TODO Create your models here.
# TODO 实现添加和查找账户信息的功能
# TODO 自定义管理器
class PassportManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)

    # TODO 添加一个账户信息
    def add_one_passport(self, username, password, email):
        passport = self.create(username=username, password=get_hash(password), email=email)
        return passport

    # TODO 根据账户信息查找密码
    def get_one_passport(self, username, password):
        try:
            passport = self.get(username=username, password=get_hash(password))
        except self.model.DoesNotExist:
            # TODO 账户不存在
            passport = None
        return passport


# 实现地址模型的管理器
class AddressManager(models.Manager):

    def get_default_address(self, passport_id):
        """查询指定用户的默认收货地址"""
        try:
            addr = self.get(passport_id=passport_id, is_default=True)
        except self.model.DoesNotExist:
            # 没有默认收货地址
            addr = None
        return addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr, zip_code, recipient_phone):
        # 添加收货地址
        # 判断用户是否有默认收货地址
        addr = self.get_default_address(passport_id=passport_id)

        if addr:
            # 存在默认地址
            is_default = False
        else:
            # 不存在默认地址
            is_default = True

        # 添加一个地址
        addr = self.create(passport_id=passport_id,
            recipient_name=recipient_name,
            recipient_addr=recipient_addr,
            zip_code=zip_code,
            recipient_phone=recipient_phone,
            is_default=is_default)


        return addr


class Passport(BaseModel):
    # 用户模型类
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='用户密码')
    email = models.EmailField(verbose_name='用户邮箱')
    is_active = models.BooleanField(default=False, verbose_name='激活状态')
    # TODO 使用自定义的管理器
    objects = PassportManger()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 's_user_account'

    def __str__(self):
        return self.username


# todo 创建用户地址的表
class Address(BaseModel):
    """地址模型类"""
    recipient_name = models.CharField(max_length=100, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=300, verbose_name='收件人地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
    recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    passport = models.ForeignKey('Passport', verbose_name='账户')

    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name

    def  __str__(self):
        return self.recipient_name

