from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

import jsonfield

class Category(models.Model):
  name = models.CharField(max_length=64,unique=True)
  json_fields = ['name','id']
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ("name",)

class TagManager(models.Manager):
  def get(self,*args,**kwargs):
    if 'name' in kwargs:
      kwargs['name'] = slugify(kwargs['name'])
    return super(TagManager,self).get(*args,**kwargs)

class Tag(models.Model):
  json_fields = ['name','id']
  name = models.CharField(max_length=64,unique=True)
  categories = models.ManyToManyField(Category)
  _ht = "Non-approved tags may be deleted if they aren't up to standards."
  approved = models.BooleanField(default=False,help_text=_ht)
  objects = TagManager()
  __unicode__ = lambda self: self.name
  def save(self,*args,**kwargs):
    self.name = slugify(self.name)
    super(Tag,self).save(*args,**kwargs)
  class Meta:
    ordering = ("name",)

class Post(models.Model):
  json_fields = ['name','id','tag_ids', 'data']
  name = models.CharField(max_length=256)
  tags = models.ManyToManyField(Tag)
  categories = models.ManyToManyField(Category)
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  closed = models.DateTimeField(null=True,blank=True)
  data = jsonfield.JSONField(default={})
  __unicode__ = lambda self: self.name
  tag_ids = property(lambda self: list(self.tags.values_list("id",flat=True)))
  category_ids = property(lambda self: list(self.categories.values_list("id",flat=True)))
  class Meta:
    ordering = ("-created",)
