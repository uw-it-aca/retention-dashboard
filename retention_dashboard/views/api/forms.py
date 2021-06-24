# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django import forms
from retention_dashboard.dao.admin import GCSDataDao


class BulkDataForm(forms.Form):
    delete_existing_data = forms.BooleanField()
    upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.zip'}))


class GCSForm(forms.Form):
    dao = GCSDataDao()
    gcs_rad_files = dao.get_files_list()
    file = forms.ChoiceField(choices=gcs_rad_files)
