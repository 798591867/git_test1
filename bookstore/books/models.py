from db.base_model import BaseModel
from tinymce.models import HTMLField
from books.enums import *
from django.db import models


class BooksManager(models.Manager):
    """商品模型管理器"""
    # sort='new'        按照创建时间进行排序
    # sort='hot'        按照商品销量进行排序
    # sort='price'      按照商品的价格进行排序
    # sort=''           按照默认顺序排序
    def get_books_by_type(self, type_id, limit=None, sort='default'):
        """根据商品类型ｉｄ查询商品的信息"""
        if sort == 'new':
            order_by = ('-create_time',)
        elif sort == 'hot':
            order_by = ('-sales',)
        elif sort == 'price':
            order_by = ('price',)
        else:
            order_by = ('-pk', ) # 按照primary key降序排列

        # TODO　查询数据
        books_li = self.filter(type_id=type_id).order_by(*order_by)

        # 查询结果集的限制
        if limit:
            books_li = books_li[:limit]
        return  books_li

    def get_books_by_id(self, books_id):
        """根据商品的信息"""
        try:
            books = self.get(id=books_id)
        except self.model.DoesNotExist:
            # 不存在商品信息
            books = None
        return books

class Books(BaseModel):
    # TODO 商品的模型类
    books_type_choices = ((k, v) for k, v in BOOKS_TYPE.items())
    status_choices = ((k, v) for k, v in STATUS_CHOICE.items())
    type_id = models.SmallIntegerField(default=PYTHON, choices=books_type_choices, verbose_name='商品种类')
    name = models.CharField(max_length=100, verbose_name='商品名称')
    desc = models.CharField(max_length=200, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    stock = models.IntegerField(default=100, verbose_name='商品库存')
    sales = models.IntegerField(default=100, verbose_name='商品销量')
    detail = HTMLField(verbose_name='商品详情')
    image = models.ImageField(upload_to='books', verbose_name='商品图片')
    status = models.SmallIntegerField(default=ONLINE, choices=status_choices, verbose_name='商品状态')


# for i in range(100):
#     book = Books()
#     book.name='python大法好'+str(i)
#     book.desc = 'python大法好,好啊真是好'
#     book.price = 100+i
#     book.unite = '本'
#     book.stock = i*100
#     book.sales = i*200
#     book.detail = 'python大法好,好啊真是好'*i
#     book.image = 'books/book00%d.jpg' % (i+1)
#     book.save()



    objects = BooksManager()

    class Meta:
        db_table = 's_books'
        verbose_name = '书籍信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name