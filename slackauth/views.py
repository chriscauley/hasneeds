from functools import partial
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from slackclient import SlackClient

@partial
def get_team(backend, details, response, is_new=False, *args, **kwargs):
  if backend.name == 'slack' and is_new:
    token = response['access_token']
    sc = SlackClient(token)
    team = sc.api_call("team.info")['team']
    if team['domain'] not in settings.ALLOWED_SLACK_DOMAINS:
      return HttpResponseRedirect("/slack-domain-not-allowed/?domain=%s"%team['domain'])
    User = get_user_model()
    username = details['username'].split("@")[0]
    if User.objects.filter(username=username):
      username = details['username']
    return { 'username': username }

def not_allowed(request):
  return TemplateResponse(request,"slack-domain-not-allowed.html",{})
