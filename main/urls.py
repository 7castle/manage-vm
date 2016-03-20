from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^create/$', views.create_vm, name='create_vm'),
  url(r'^manage/$', views.manage, name='manage'),
]
