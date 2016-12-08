from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.views.static import serve
from main import views as main_views

import social.apps.django_app.urls
import slackauth.urls
import lablackey.urls

admin.autodiscover()

urlpatterns = [
  url(r'^admin/', include(admin.site.urls)),
  url(r'^auth/',include(auth_urls)),

  url(r'^$', main_views.home,name='home'),
  url(r'favicon.ico$', main_views.redirect, {'url': getattr(settings,'FAVICON','/static/favicon.png')}),
  url('', include(social.apps.django_app.urls, namespace='social')),
  url('', include(slackauth.urls)),
  url('', include(lablackey.urls)),
]

if settings.DEBUG:
  urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
  ]
