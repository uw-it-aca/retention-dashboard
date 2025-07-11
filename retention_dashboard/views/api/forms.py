# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django import forms
from retention_dashboard.dao.admin import StorageDao
from retention_dashboard.models import Week


class LocalDataForm(forms.Form):
    local_upload_week = forms.ChoiceField()
    local_upload_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.csv'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        weeks = Week.objects.all()
        week_choices = []
        for week in weeks:
            week_choices.append(
                (week.id,
                 f"{week.year} - {week.get_quarter_display()} "
                 f"- Week {week.number}"))
        self.fields['local_upload_week'].choices = week_choices


class StorageForm(forms.Form):

    gcs_file = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            dao = StorageDao()
            rad_files = dao.get_files_list()
            file_choices = []
            for file_name in rad_files:
                file_choices.append((file_name, file_name))
            self.fields['gcs_file'].choices = file_choices
        except Exception as err:
            logging.error(err)
            logging.error("Unable to load RAD file choices")
