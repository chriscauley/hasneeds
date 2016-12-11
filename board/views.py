from django.http import JsonResponse
from django.template.defaultfilters import slugify

from .models import Tag

def tags(request):
  tags = Tag.objects.filter(name__icontains=slugify(request.GET['q']))
  return JsonResponse([{ 'id': t.id,'name':  t.name } for t in tags],safe=False)

def add_tag(request):
  t,new = Tag.objects.get_or_create(name=request.POST['name'])
  return JsonResponse({'id': t.id, 'name': t.name})
