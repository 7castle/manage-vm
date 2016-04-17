from django.db import models
from django.contrib.auth.models import User

class VM(models.Model):
  user = models.ForeignKey(User, related_name='user', null=False)
  vmid = models.PositiveIntegerField()   
  name = models.CharField(max_length=60)
  nodename = models.CharField(max_length=60)
  
  def __unicode__(self):
    return u'%s' % self.name

class VM_Request(models.Model):
    user = models.ForeignKey(User, null=False)
    node = models.CharField(max_length=60)
    name = models.CharField(max_length=60)
    ostype = models.CharField(max_length=60)
    iso = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    disk_format = models.CharField(max_length=60)
    cores = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()
    net_model = models.CharField(max_length=60)
    bridge = models.CharField(max_length=10)
    request_time = models.DateTimeField()

class VM_Limits(models.Model):
    memory = models.PositiveIntegerField()
    cores = models.PositiveSmallIntegerField()
    disk_size = models.PositiveSmallIntegerField()
    sockets = models.PositiveSmallIntegerField()
