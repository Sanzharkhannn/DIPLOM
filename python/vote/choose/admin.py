from django.contrib import admin
from .models import Content, Vote  # Импортируем модели, а не формы
from .models import UserRSAKeys

# Регистрируем модели в админке
admin.site.register(Content)
admin.site.register(Vote)
@admin.register(UserRSAKeys)
class UserRSAKeysAdmin(admin.ModelAdmin):
    list_display = ('user',)
