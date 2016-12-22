from django.conf import settings
from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.views.static import serve
from main import views as main_views

import social.apps.django_app.urls
import slackauth.urls
import lablackey.urls, lablackey.views

import board.views

admin.autodiscover()

urlpatterns = [
  url(r'^admin/', include(admin.site.urls)),
  url(r'^auth/',include(auth_urls)),

  url(r'^(|post/new/|post|tag|category)$', lablackey.views.single_page_app),
  url(r'^p/(\d+)/([\w\d\-]+)/', lablackey.views.single_page_app),
  url(r'^(t|c)/([\w\d\-]+)/', lablackey.views.single_page_app),
  url(r'favicon.ico$', main_views.redirect, {'url': getattr(settings,'FAVICON','/static/favicon.png')}),
  url('', include(social.apps.django_app.urls, namespace='social')),
  url('', include(slackauth.urls)),
  url('', include(lablackey.urls)),
  url('^api/board/tags/$',board.views.tags),
  url('^api/board/tag/new/$',board.views.add_tag),
  url('^api/board/post/new/$',board.views.post_post),
  url('^api/board/post/delete/(\d+)/$',board.views.delete_post),
  url('^api/board/post/edit/(\d+)/$',board.views.post_post),
]

if settings.DEBUG:
  urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
  ]
