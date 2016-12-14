from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from .models import Tag,Post

def tags(request):
  tags = Tag.objects.filter(slug__icontains=slugify(request.GET['q']))
  return JsonResponse([{'name': t.pk,'id': t.pk} for t in tags],safe=False)

def add_tag(request):
  t,new = Tag.objects.get_or_create(slug=request.POST['slug'])
  return JsonResponse({'name': t.pk,'id': t.pk})

def post_post(request,pk=None):
  user = request.user
  if request.user.is_superuser and request.POST.get('username',None):
    user = get_user_model().objects.get_or_create(username=request.POST['username'])[0]
  if pk:
    post = get_object_or_404(Post,id=pk)
    if not (post.user == user or request.user.is_superuser):
      raise NotImplementedError()
  else:
    post = Post()
  post.user=user
  post.name = request.POST['name']
  post.has_needs=request.POST['has_needs']
  post.save()
  post.tags = request.POST['tag_pks'].split(',')
  post.categories = request.POST['category_pks'].split(',')
  for k in post.data_fields:
    post.data[k] = request.POST[k]
  post.render()
  post.save()
  return JsonResponse({'ur_route_to': post.get_absolute_url()})
