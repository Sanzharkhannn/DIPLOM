from django.db import models
from django.contrib.auth.models import User



class Poll(models.Model):
    question = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class VoteOpt(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)


'''

class Option(models.Model):
    name = models.CharField(max_length=100)
    total_votes = models.PositiveIntegerField(default=0)


class VoteOpt(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

'''