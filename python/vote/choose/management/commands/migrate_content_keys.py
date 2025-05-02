from django.core.management.base import BaseCommand
from choose.models import Content
from choose.models import UserRSAKeys  # укажи правильный путь

class Command(BaseCommand):
    help = "Заполняет ключи RSA из UserRSAKeys в Content, если они пустые"

    def handle(self, *args, **kwargs):
        contents = Content.objects.filter(public_key='')
        self.stdout.write(f"Найдено {contents.count()} Content без ключей")

        for content in contents:
            try:
                user_keys = UserRSAKeys.objects.get(user=content.user)
                content.public_key = user_keys.public_key
                content.private_key_encrypted = user_keys.private_key_encrypted
                content.save()
                self.stdout.write(f"✓ Ключи добавлены для Content #{content.id}")
            except UserRSAKeys.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"[!] У пользователя {content.user.username} нет ключей, пропускаем"
                ))

        self.stdout.write(self.style.SUCCESS("Все доступные ключи перенесены."))
