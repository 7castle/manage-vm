from django.db import models
from django.contrib.auth.models import User

class VM(models.Model):
  user = models.ForeignKey(User, related_name='user', null=False)
  vmid = models.PositiveIntegerField()   
  name = models.CharField(max_length=60)
  nodename = models.CharField(max_length=60)

  def __unicode__(self):
    return u'%s' % self.name

class VM_Limits(models.Model):
    memory = models.PositiveIntegerField()
    cores = models.PositiveSmallIntegerField()
    disk_size = models.PositiveSmallIntegerField()
    sockets = models.PositiveSmallIntegerField()
