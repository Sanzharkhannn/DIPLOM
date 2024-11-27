from django.contrib import admin
from .models import Content, Vote  # Импортируем модели, а не формы

# Регистрируем модели в админке
admin.site.register(Content)
admin.site.register(Vote)
