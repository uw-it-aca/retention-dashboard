# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django import forms


class BulkDataForm(forms.Form):
    delete_existing_data = forms.BooleanField()
    upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.zip'}))
