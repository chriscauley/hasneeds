from django.conf import settings
from django.db import models

from jsonfield import JSONField

class SlackObject(models.Model):
  id = models.CharField(max_length=12,primary_key=True)
  name = models.CharField(max_length=128)
  data = JSONField(default=dict)
  object_type = models.CharField(max_length=64)
  updated = models.DateTimeField(auto_now=True)
  __unicode__ = lambda self: self.name
  @classmethod
  def ninja_add(clss,json):
    object_type = "channel" #this will eventually need to be set either by an argument or by evaluating content of json
    obj,new = clss.objects.get_or_create(id=json['id'],name=json['name'],object_type=object_type)
    if new:
      print "created: %s"%obj.name
    obj.data = json
    obj.save()

class SlackUser(models.Model):
  id = models.CharField(max_length=12,primary_key=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True)
  data = JSONField(default=dict)
  updated = models.DateTimeField(auto_now=True)

class SlackMessage(models.Model):
  data = JSONField(default=dict)
  channel = models.ForeignKey(SlackObject)
  slackuser = models.ForeignKey(SlackUser)
  ts = models.CharField(max_length=20) # timestamp, used with slackuser and channel to ensure uniqueness
  @classmethod
  def ninja_add(clss,json,channel):
    slackuser = SlackUser.objects.get_or_create(id=json['user'])[0]
    obj,new = clss.objects.get_or_create(channel=channel,ts=json['ts'],slackuser=slackuser)
