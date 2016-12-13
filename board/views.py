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

def add_post(request):
  user = request.user
  if request.user.is_superuser and request.POST.get('username',None):
    user = get_user_model().objects.get_or_create(username=request.POST['username'])[0]
  post = Post.objects.create(
    user=user,
    name=request.POST['name']
  )
  post.data['description'] = request.POST['description']
  post.data['external_url'] = request.POST['external_url']
  post.tags = request.POST['tag_pks'].split(',')
  post.categories = request.POST['category_pks'].split(',')
  post.render()
  post.save()
  return JsonResponse({'ur_route_to': post.get_absolute_url()})

def edit_post(request,pk):
  user = request.user
  post = get_object_or_404(Post,id=pk)
  if not (post.user == user or request.user.is_superuser):
    raise NotImplementedError()
  post.name = request.POST['name']
  post.data['description'] = request.POST['description']
  post.data['external_url'] = request.POST['external_url']
  post.tags = request.POST['tag_pks'].split(',')
  post.categories = request.POST['category_pks'].split(',')
  post.render()
  post.save()
  return JsonResponse({'ur_route_to': post.get_absolute_url()})
