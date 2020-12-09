from django import forms


class BulkDataForm(forms.Form):
    delete_existing_data = forms.BooleanField()
    upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.zip'}))
