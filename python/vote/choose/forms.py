from django import forms
from .models import Poll, Option

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']
