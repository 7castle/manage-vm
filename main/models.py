from django.db import models
from django.contrib.auth.models import User

class Disk(models.Model):
  disk_name = models.CharField(max_length=20)
  storage_domain = models.CharField(max_length=100)
  size = models.IntegerField()
  status = models.CharField(max_length=20, null=True)
  interface = models.CharField(max_length=50)
  format = models.CharField(max_length=50)
  bootable = models.BooleanField()

  def __unicode__(self):
    return u'%s' % self.disk_name

class NIC(models.Model):
  name = models.CharField(max_length=20)
  network = models.CharField(max_length=50)
  interface = models.CharField(max_length=20)
  
  def __unicode__(self):
    return u'%s' % self.name

class VM(models.Model):
  user = models.ForeignKey(User, related_name='user', null=False)
  vm_name = models.CharField(max_length=30)
  description = models.CharField(max_length=200)
  memory = models.IntegerField()
  cores = models.IntegerField()
  cluster = models.CharField(max_length=100)
  template = models.CharField(max_length=100)
  disk = models.ForeignKey(Disk, related_name='disk', null=False)
  nic = models.ForeignKey(NIC, related_name='nic', null=False)

  def __unicode__(self):
    return u'%s' % self.vm_name
