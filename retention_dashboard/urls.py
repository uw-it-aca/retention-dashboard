from django.urls import re_path, include
from retention_dashboard.views import (LandingView,
                                       DataView,
                                       AdminView,
                                       WeekAdmin,
                                       DataAdmin)


urlpatterns = [

    re_path(r'^api/data/(?P<week>.*)/(?P<file>.*)/',
            DataView.as_view(),
            name="data_view"),
    re_path(r'^api/admin/week/',
            WeekAdmin.as_view(),
            name="data_view"),
    re_path(r'^api/admin/dataset/(?P<upload_id>[0-9]+)/',
            DataAdmin.as_view(),
            name="data_view"),
    re_path(r'^api/admin/dataset/',
            DataAdmin.as_view(),
            name="data_view"),
    re_path(r'^admin/', AdminView.as_view()),
    re_path(r'^', LandingView.as_view()),
]
