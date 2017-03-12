from django.contrib import admin

from .models import SlackObject, SlackUser, SlackMessage

class SlackAdmin(admin.ModelAdmin):
  readonly_fields = ['data']

@admin.register(SlackObject)
class SlackObjectAdmin(SlackAdmin):
  pass

@admin.register(SlackUser)
class SlackUserAdmin(SlackAdmin):
  pass

@admin.register(SlackMessage)
class SlackMessageAdmin(SlackAdmin):
  pass
