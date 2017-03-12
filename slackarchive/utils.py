from django.conf import settings

from .models import SlackObject, SlackUser, SlackMessage

from slackclient import SlackClient

def create_channels():
  sc = SlackClient(settings.SLACK_TOKEN)
  channels_list = sc.api_call("channels.list")
  for channel in channels_list['channels']:
    SlackObject.ninja_add(channel)

def log_channels():
  i = 0
  sc = SlackClient(settings.SLACK_TOKEN)
  for channel in SlackObject.objects.filter(object_type="channel").order_by('updated'):
    if i > 10:
      break
    d1 = channel.updated
    message_count = channel.slackmessage_set.count()
    channel.save()
    print  channel.updated-d1,'\t',channel
    history = sc.api_call("channels.history",channel=channel.id)
    for m in history['messages']:
      if not 'user' in m:
        if not 'bot_id' in m:
          print "BAD MESSAGE:\n%s\n\n"%m
        continue
      SlackMessage.ninja_add(m,channel)
    i += 1
    print channel,message_count,channel.slackmessage_set.count()
    
