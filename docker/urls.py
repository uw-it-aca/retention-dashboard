from .base_urls import *
from django.conf.urls import include
from django.urls import re_path

urlpatterns += [
    re_path('^', include('retention_dashboard.urls'))
]
