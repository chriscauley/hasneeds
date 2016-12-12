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
  data = {k:request.POST[k] for k in ['categories','tags','name','description'] if k in request.POST}
  post = Post.objects.create(
    user=request.user,
    **data
  )
  return JsonResponse({'ur_route_to': post.get_absoluet_url()})
