from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.contrib.auth.forms import UserCreationForm  # type: ignore
from django import forms  # type: ignore


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# class Content(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contents')
#     title = models.CharField(max_length=200)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     start_date = models.DateField(null=True, blank=True)
#     end_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return self.title

class Content(models.Model):
    user       = models.ForeignKey(User,
                     on_delete=models.CASCADE,
                     related_name='user_contents')
    title      = models.CharField(max_length=200)
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date   = models.DateField(null=True, blank=True)

    # вот они — асимметричные ключи для данного опроса
    public_key            = models.TextField(
                              blank=True,
                              help_text="PEM публичного ключа"
                            )
    private_key_encrypted = models.TextField(
                              blank=True,
                              help_text="PEM приватного ключа, зашифрованный MASTER_KEY"
                            )

    def __str__(self):
        return self.title

class ContentOption(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200)

    def __str__(self):
        return f"Option: {self.option_text} (for {self.content.title})"

# Голоса за варианты
class ContentOptionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(ContentOption, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'option')  # Чтобы пользователь не мог голосовать дважды за один вариант

    def __str__(self):
        return f"{self.user.username} проголосовал за {self.option.option_text}"

class EncryptedVote(models.Model):
    content          = models.ForeignKey(Content,
                         on_delete=models.CASCADE,
                         related_name='encrypted_votes')
    # здесь лежит base64(rsa_oaep(option_id)) или base64(rsa_oaep(option_text))
    encrypted_choice = models.TextField()
    voted_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"EncryptedVote for poll #{self.content.id} at {self.voted_at}"


# Оставляем твой класс Vote для лайков/дизлайков
class Vote(models.Model):
    VOTE_TYPE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )

    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.content:
            return f"{self.voter} {self.vote_type} for content {self.content}"
        return f"{self.voter} {self.vote_type} for user {self.target_user}"


# RSA для безопасности, оставляем без изменений
class UserRSAKeys(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.TextField()
    private_key_encrypted = models.TextField()  # Лучше хранить зашифрованным


class PollResult(models.Model):
    # связываем результат с опросом (Content)
    content     = models.ForeignKey(
                     Content,
                     on_delete=models.CASCADE,
                     related_name='results'
                   )
    # вариант ответа – сохраняем текст опции
    option_text = models.CharField(max_length=200)
    votes       = models.IntegerField(default=0)

    class Meta:
        unique_together = ('content', 'option_text')

    def __str__(self):
        return f"{self.content.title!r}: {self.option_text} → {self.votes}"