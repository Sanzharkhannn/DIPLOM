from django.db import models
from django.contrib.auth.models import User

class Option(models.Model):
    name = models.CharField(max_length=100)
    total_votes = models.PositiveIntegerField(default=0)

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name