from django import forms
from .models import RandomPost


class RandomPostForm(forms.ModelForm):
    class Meta:
        model = RandomPost
        fields = ['title', 'description', 'photo']
