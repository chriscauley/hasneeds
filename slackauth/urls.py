from django.conf.urls import url

import views

urlpatterns = [
  url(r'^slack-domain-not-allowed/$',views.not_allowed),
]
