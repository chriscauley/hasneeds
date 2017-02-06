from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

import jsonfield, markdown, re

from lablackey.unrest import JsonMixin

urlfinder = re.compile('^(http:\/\/\S+)')
urlfinder2 = re.compile('\s(http:\/\/\S+)')

def urlify(value):
  value = urlfinder.sub(r'<\1>', value)
  return urlfinder2.sub(r' <\1>', value)

class Category(models.Model,JsonMixin):
  name = models.CharField(max_length=64)
  slug = models.CharField(max_length=64,primary_key=True)
  def save(self,*args,**kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super(Category,self).save(*args,**kwargs)
  __unicode__ = lambda self: self.slug
  get_absolute_url = lambda self: "/t/%s/"%self.slug
  class Meta:
    ordering = ("slug",)

class TagManager(models.Manager):
  def get(self,*args,**kwargs):
    if 'name' in kwargs:
      kwargs['name'] = slugify(kwargs['name'])
    return super(TagManager,self).get(*args,**kwargs)

class Tag(models.Model,JsonMixin):
  slug = models.CharField(max_length=64,primary_key=True)
  categories = models.ManyToManyField(Category)
  _ht = "Non-approved tags may be deleted if they aren't up to standards."
  approved = models.BooleanField(default=False,help_text=_ht)
  objects = TagManager()
  __unicode__ = lambda self: self.slug
  get_absolute_url = lambda self: "/t/%s/"%self.pk
  def save(self,*args,**kwargs):
    self.slug = slugify(self.slug)
    super(Tag,self).save(*args,**kwargs)
  class Meta:
    ordering = ("slug",)

HAS_NEEDS_CHOICES = [
  ('has', 'I have...'),
  ('needs', 'I need...')
]

class Post(models.Model,JsonMixin):
  name = models.CharField(max_length=256)
  tags = models.ManyToManyField(Tag)
  categories = models.ManyToManyField(Category)
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  closed = models.DateTimeField(null=True,blank=True)
  data = jsonfield.JSONField(default={})
  has_needs = models.CharField(max_length=8,choices=HAS_NEEDS_CHOICES,default="has")
  __unicode__ = lambda self: self.name

  json_fields = ['name','id', 'data', 'category_pks', 'tag_pks', 'username', 'has_needs', 'closed']
  data_fields = ['description','external_url']
  filter_fields = ['categories__slug', 'tags__slug', 'has_needs']
  tag_pks = property(lambda self: list(self.tags.values_list("pk",flat=True)))
  category_pks = property(lambda self: list(self.categories.values_list("pk",flat=True)))
  username = property(lambda self: self.user.username)
  get_absolute_url = lambda self: "/p/%s/%s/"%(self.pk,slugify(self.name))
  class Meta:
    ordering = ("-created",)
  def render(self):
    self.data['rendered'] = markdown.markdown(urlify(self.data['description']))

