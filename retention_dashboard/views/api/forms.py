from django import forms


class BulkDataForm(forms.Form):
    upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.zip'}))
    skip_unknown_files = forms.BooleanField(required=False)
