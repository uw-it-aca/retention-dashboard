# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path
from retention_dashboard.views.pages import LandingView, AdminView
from retention_dashboard.views.api.admin import (WeekAdmin,
                                                 DataAdmin,
                                                 BulkDataAdmin,
                                                 MockDataAdmin)
from retention_dashboard.views.api.data import (DataView,
                                                WeekView,
                                                DataAuthView,
                                                FilteredDataView,
                                                AdvisorListView)


urlpatterns = [
    re_path(r'api/v1/weeks/', WeekView.as_view(), name="week_view"),
    re_path(r'api/v1/advisors/', AdvisorListView.as_view(),
            name="advisor_view"),
    re_path(r'api/v1/data_auth/', DataAuthView.as_view(),
            name="data_auth_view"),
    re_path(r'api/v1/filtered_data/', FilteredDataView.as_view(),
            name="filtered_view"),
    re_path(r'^api/data/(?P<week>.*)/(?P<file>.*)/',
            DataView.as_view(),
            name="data_view"),
    re_path(r'^api/admin/week/',
            WeekAdmin.as_view(),
            name="week_admin_view"),
    re_path(r'^api/admin/dataset/(?P<upload_id>[0-9]+)/',
            DataAdmin.as_view(),
            name="dataset_admin_delete_view"),
    re_path(r'^api/admin/mock_data/',
            MockDataAdmin.as_view(),
            name="mocK_admin_view"),
    re_path(r'^api/admin/dataset/',
            DataAdmin.as_view(),
            name="dataset_admin_view"),
    re_path(r'^api/admin/bulk_dataset/$',
            BulkDataAdmin.as_view(),
            name="bulk_dataset_admin_view"),
    re_path(r'^admin/?$', AdminView.as_view()),
    re_path(r'^', LandingView.as_view()),
]
