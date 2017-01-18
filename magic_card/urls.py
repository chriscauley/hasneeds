from django.conf.urls import url

import magic_card.views

urlpatterns = [
  url(r'^load-meta-data/',magic_card.views.load_meta_data)
]
