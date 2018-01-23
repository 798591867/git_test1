from django.conf.urls import  url
from books import views

urlpatterns = [
    url(r'^index/$', views.index, name='book_index'),
    url(r'^(?P<books_id>\d)+/$', views.detail, name='book_detail'),
]
