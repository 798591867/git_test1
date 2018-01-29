from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^info_center/$', views.user, name='info_center'),
    url(r'^order/$', views.order, name='order'),
    url(r'^address/$', views.address, name='address'),

]
