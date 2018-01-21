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
            passport = self.get(username=username, password=password)
        except self.model.DoesNotExist:
            # TODO 账户不存在
            passport = None
        return passport


class Passport(BaseModel):
    # 用户模型类
    username = models.CharField(max_length=20, verbose_name='用户名')
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
