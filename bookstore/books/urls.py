from django.conf.urls import  url
from books import views

urlpatterns = [
    url(r'^index/$', views.index, name='book_index'),
    url(r'^(?P<books_id>\d+)/$', views.detail, name='book_detail'),  # 配置详情页路由
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)/$', views.list, name = 'list') # 列表页

]
