from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^register_handle', views.register_handle, name='register_handle'),
]
