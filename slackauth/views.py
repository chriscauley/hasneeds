from functools import partial
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from slackclient import SlackClient

@partial
def get_team(backend, details, response, is_new=False, *args, **kwargs):
  if backend.name != 'slack': # not my problem!
    return
  social = kwargs.get('social') or backend.strategy.storage.user.get_social_auth(backend.name, uid)
  needs_team = social and not social.extra_data.get("team")
  if needs_team or is_new:
    token = response['access_token']
    sc = SlackClient(token)
    team = sc.api_call("team.info")['team']
    if team['domain'] not in settings.ALLOWED_SLACK_DOMAINS:
      return HttpResponseRedirect("/slack-domain-not-allowed/?domain=%s"%team['domain'])
    social.set_extra_data({'team': team['domain']})
    social.save()
    User = get_user_model()
    username = details['username'].split("@")[0]
    if User.objects.filter(username=username):
      username = details['username']
    return { 'username': username }

def not_allowed(request):
  return TemplateResponse(request,"slack-domain-not-allowed.html",{})

def slack_redirect(request,username):
  user = get_object_or_404(get_user_model(),username=username)
  team = user.social_auth.filter(provider="slack")[0].extra_data['team']
  return HttpResponseRedirect("https://%s.slack.com/messages/@%s"%(team,username))
