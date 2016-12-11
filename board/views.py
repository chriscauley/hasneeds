from django.http import JsonResponse
from django.template.defaultfilters import slugify

from .models import Tag

def tags(request):
  tags = Tag.objects.filter(name__icontains=slugify(request.GET['q']))
  return JsonResponse([{ 'id': t.id,'name':  t.name } for t in tags],safe=False)
