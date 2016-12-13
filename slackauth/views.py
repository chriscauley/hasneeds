from functools import partial
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from slackclient import SlackClient

def associate_by_slack_name(backend, details, user=None, *args, **kwargs):
  """
  Associate pre-existing users by slack name. Useful for prepopulating data from slack api.
  Not recommended if multiple slack domains are used.
  """
  if user:
    return
  username = details['username']
  if backend.strategy.storage.user.user_exists(username=username):
    return {'user':backend.strategy.storage.user.get_user(username=username),'is_new': False}

@partial
def validate_team(backend, details, response, is_new=False, *args, **kwargs):
  if backend.name == 'slack' and is_new:
    domain = response['url'].split("//")[-1].split(".slack.com")[0]
    if domain not in settings.ALLOWED_SLACK_DOMAINS:
      return HttpResponseRedirect("/slack-domain-not-allowed/?domain=%s"%domain)

def set_team(backend, details, response, is_new, user=None, *args, **kwargs):
  if backend.name == 'slack' and not 'team' in kwargs['social'].extra_data:
    domain = response['url'].split("//")[-1].split(".slack.com")[0]
    social = kwargs['social']
    team_keys = ['team','team_name','url']
    team = {k: response[k] for k in team_keys}
    team['domain'] = domain
    social.set_extra_data({"team":team})
    social.save()

def not_allowed(request):
  if request.user.is_authenticated():
    # otherwise they land on this page after they fail once and then log in for real
    return HttpResponseRedirect("/")
  return TemplateResponse(request,"slack-domain-not-allowed.html",{})

def slack_redirect(request,username):
  user = get_object_or_404(get_user_model(),username=username)
  team = user.social_auth.filter(provider="slack")[0].extra_data['team']
  return HttpResponseRedirect("%smessages/@%s"%(team['url'],username))
