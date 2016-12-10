from graphene_django import DjangoObjectType
import graphene

from .models import Post, Tag, Category

class PostNode(DjangoObjectType):
  class Meta:
    model = Post

class BoardQuery(graphene.AbstractType):
  posts = graphene.List(PostNode)
