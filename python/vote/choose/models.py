from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django import forms # type: ignore


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contents')
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
   VOTE_TYPE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),)
   
   voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')  # Кто голосует
   content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')  # За контент
   target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_votes')  # За пользователя
   vote_type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       if self.content:
           return f"{self.voter} voted {self.vote_type} on content {self.content}"
       return f"{self.voter} voted {self.vote_type} for user {self.target_user}"

