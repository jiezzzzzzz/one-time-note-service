from django import forms
from .models import Note


class TextForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']