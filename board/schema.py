from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene.types.json import JSONString
import graphene, jsonfield

@convert_django_field.register(jsonfield.JSONField)
def convert_jsonfield(field,registry=None):
  return JSONString(description=field.help_text, required=not field.null)

from .models import Post, Tag, Category

class PostNode(DjangoObjectType):
  class Meta:
    model = Post
    interfaces = (graphene.relay.Node,)

class UserNode(DjangoObjectType):
  class Meta:
    model = get_user_model()
    interfaces = (graphene.relay.Node,)

class Query(graphene.ObjectType):
  all_posts = DjangoFilterConnectionField(PostNode)
  user = graphene.relay.Node.Field(UserNode)

schema = graphene.Schema(query=Query)
