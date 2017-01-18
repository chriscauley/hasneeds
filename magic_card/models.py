from django.db import models

import jsonfield

class Url(models.Model):
  url = models.CharField(max_length=2083)
  domain = models.CharField(max_length=256,null=True,blank=True)
  data = jsonfield.JSONField(default=dict)
  created = models.DateTimeField(auto_now_add=True)
  error = models.CharField(null=True,blank=True,max_length=64)
  __unicode__ = lambda self: self.url[:100]
  class Meta:
    ordering = ('-created',)
