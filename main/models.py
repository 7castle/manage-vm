from django.db import models
from django.contrib.auth.models import User

class Disk(models.Model):
  storage_domain = models.CharField(max_length=100)
  size = models.IntegerField()
  status = models.CharField(max_length=20, null=True)
  interface = models.CharField(max_length=50)
  format = models.CharField(max_length=50)
  bootable = models.BooleanField()

class NIC(models.Model):
  name = models.CharField(max_length=20)
  network = models.CharField(max_length=50)
  interface = models.CharField(max_length=20)

class VM(models.Model):
  user = models.ForeignKey(User, related_name='user', null=False)
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=200)
  memory = models.IntegerField()
  cores = models.IntegerField()
  cluster = models.CharField(max_length=100)
  template = models.CharField(max_length=100)
  disk = models.ForeignKey(Disk, related_name='disk', null=False)
  nic = models.ForeignKey(NIC, related_name='nic', null=False) 
