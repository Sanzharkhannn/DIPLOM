from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from choose.models import UserRSAKeys
from Cryptodome.PublicKey import RSA

class Command(BaseCommand):
    help = 'Генерирует RSA-ключи для всех существующих пользователей'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'userrsakeys'):
                key = RSA.generate(2048)
                private_key = key.export_key().decode()
                public_key = key.publickey().export_key().decode()

                UserRSAKeys.objects.create(
                    user=user,
                    public_key=public_key,
                    private_key_encrypted=private_key  # лучше шифровать
                )
                self.stdout.write(self.style.SUCCESS(f'Ключи созданы для пользователя {user.username}'))
            else:
                self.stdout.write(f'Ключи уже существуют для {user.username}')

