from django.db import models
from django.contrib.auth.models import User

class VM(models.Model):
  user = models.ForeignKey(User, related_name='user', null=False)
  vmid = models.PositiveIntegerField()
  template = models.CharField(max_length=100)
  hostname = models.CharField(max_length=30)
  storage = models.CharField(max_length=50)
  memory = models.PositiveIntegerField()
  swap = models.PositiveIntegerField()
  cores = models.PositiveSmallIntegerField()
  disk = models.PositiveIntegerField()
  description = models.CharField(max_length=200)
  ip = models.CharField(max_length=15)
  status = models.CharField(max_length=20)

  def __unicode__(self):
    return u'%s' % self.hostname
