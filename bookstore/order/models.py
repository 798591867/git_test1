from django.db import models
from db.base_model import BaseModel
from .enums import *


# Create your models here.


class OrderInfo(BaseModel):
    # 订单信息模型类
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name='订单编号')
    passport = models.ForeignKey('users.Passport', verbose_name='下单账户')
    addr = models.ForeignKey('users.Address', verbose_name='收货地址')
    total_count = models.IntegerField(default=1, verbose_name='商品总数')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单运费')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='支付方式')
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付编号')

    class Meta:
        db_table = 's_order_info'
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id


class OrderBooks(BaseModel):
    # 订单商品模型类
    order = models.ForeignKey('OrderInfo', verbose_name='所属订单')
    books = models.ForeignKey('books.Books', verbose_name='订单商品')
    count = models.IntegerField(default=1, verbose_name='商品数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')


    class Meta:
        db_table = 's_order_books'
        verbose_name = '所属订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order