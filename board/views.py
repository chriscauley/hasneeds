from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.template.defaultfilters import slugify

from .models import Tag,Post

def tags(request):
  tags = Tag.objects.filter(name__icontains=slugify(request.GET['q']))
  return JsonResponse([t.as_json for t in tags],safe=False)

def add_tag(request):
  t,new = Tag.objects.get_or_create(name=request.POST['name'])
  return JsonResponse(t.as_json)

def add_post(request):
  user = request.user
  if request.user.is_superuser and request.POST.get('username',None):
    user = get_user_model().objects.get_or_create(username=request.POST['username'])[0]
  post = Post.objects.create(
    user=user,
    name=request.POST['name']
  )
  post.data['description'] = request.POST['description'].split(',')
  post.tags = request.POST['tags'].split(',')
  post.categories = request.POST['categories']
  return JsonResponse({'ur_route_to': post.get_absolute_url()})
