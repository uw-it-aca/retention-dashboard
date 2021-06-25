# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django import forms
from retention_dashboard.dao.admin import GCSDataDao
from retention_dashboard.dao.data import FilterDataDao
from retention_dashboard.models import Week


class LocalDataForm(forms.Form):
    dao = FilterDataDao()
    weeks = Week.objects.all()
    week_choices = []
    for week in weeks:
        week_choices.append(
            (week.id,
             f"{week.year} - {week.get_quarter_display()} "
             f"- Week {week.number}"))
    local_upload_week = forms.ChoiceField(choices=week_choices)
    local_upload_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'}))


class GCSForm(forms.Form):
    dao = GCSDataDao()
    gcs_rad_files = dao.get_files_list()
    file_choices = []
    for file_name in gcs_rad_files:
        file_choices.append((file_name, file_name))
    gcs_file = forms.ChoiceField(choices=file_choices)
