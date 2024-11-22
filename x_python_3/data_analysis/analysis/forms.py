import os

from django import forms

from .models import FileStorage


class AddFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = FileStorage
        fields = ['file',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
