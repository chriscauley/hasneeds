from django.template.response import TemplateResponse

from .models import SlackMessage

import random

def random_message(request):
  return TemplateResponse(request,"rando.xml",{'message': SlackMessage.objects.all().order_by("?")[0]})
