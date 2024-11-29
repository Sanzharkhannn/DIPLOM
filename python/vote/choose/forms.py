from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CreateContentForVote(forms.Form):
    title = forms.CharField(label="Content title", max_length=100)
    body = forms.CharField(widget=forms.Textarea)

    