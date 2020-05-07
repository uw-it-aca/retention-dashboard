from django.urls import re_path, include
from retention_dashboard.views import LandingView, DataView


urlpatterns = [

    re_path(r'^api/data/(?P<week>.*)/(?P<file>.*)/',
            DataView.as_view(),
            name="data_view"),
    re_path(r'^', LandingView.as_view()),
]
