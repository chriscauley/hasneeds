from django.conf.urls import url

import views

urlpatterns = [
  url(r'^u/([^/]+)/$',views.slack_redirect),
  url(r'^slack-domain-not-allowed/$',views.not_allowed),
]
