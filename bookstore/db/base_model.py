# bookstore/base_model.py

from django.db import models

class BaseModel(models.Model):
    # 抽象基类
    is_delete = models.BooleanField(default=0, verbose_name='删除标记')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')
    class Meta:
        abstract = True