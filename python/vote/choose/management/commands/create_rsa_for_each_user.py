# choose/management/commands/create_user_keys.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from choose.models import UserRSAKeys
from Crypto.PublicKey import RSA
from choose.crypto import encrypt_privkey

User = get_user_model()

class Command(BaseCommand):
    help = 'Генерирует RSA-ключи для всех существующих пользователей'

    def handle(self, *args, **options):
        for user in User.objects.all():
            # проверяем, есть ли уже запись
            if UserRSAKeys.objects.filter(user=user).exists():
                self.stdout.write(f'Keys already exist for {user.username}')
                continue

            # генерируем пару 2048 бит
            key = RSA.generate(2048)

            # экспортируем приватный и публичный ключи в PEM-формате (bytes)
            priv_pem_bytes = key.export_key(format='PEM')
            pub_pem_bytes  = key.publickey().export_key(format='PEM')

            # шифруем приватный ключ мастер-ключом (строкой)
            encrypted_priv = encrypt_privkey(priv_pem_bytes)

            # сохраняем в БД, приводим bytes → str
            UserRSAKeys.objects.create(
                user=user,
                public_key=pub_pem_bytes.decode('utf-8'),
                private_key_encrypted=encrypted_priv
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created keys for {user.username}'
            ))

# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
# from choose.models import UserRSAKeys
# from pycryptodome import RSA # type: ignore
# from choose.crypto import encrypt_privkey

# User = get_user_model()

# class Command(BaseCommand):
#     help = 'Генерирует RSA-ключи для всех существующих пользователей'

#     def handle(self, *args, **options):
#         for user in User.objects.all():
#             if hasattr(user, 'userrsakeys'):
#                 self.stdout.write(f'Keys already exist for {user.username}')
#                 continue

#             # генерируем пару
#             key = RSA.generate(2048)
#             priv_pem = key.export_key().decode()
#             pub_pem  = key.publickey().export_key().decode()

#             # шифруем приватный ключ мастер-ключом
#             encrypted_priv = encrypt_privkey(priv_pem)

#             UserRSAKeys.objects.create(
#                 user=user,
#                 public_key=pub_pem,
#                 private_key_encrypted=encrypted_priv
#             )
#             self.stdout.write(self.style.SUCCESS(f'Created keys for {user.username}'))



# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from choose.models import UserRSAKeys
# from Cryptodome.PublicKey import RSA

# class Command(BaseCommand):
#     help = 'Генерирует RSA-ключи для всех существующих пользователей'

#     def handle(self, *args, **kwargs):
#         users = User.objects.all()
#         for user in users:
#             if not hasattr(user, 'userrsakeys'):
#                 key = RSA.generate(2048)
#                 private_key = key.export_key().decode()
#                 public_key = key.publickey().export_key().decode()

#                 UserRSAKeys.objects.create(
#                     user=user,
#                     public_key=public_key,
#                     private_key_encrypted=private_key  # лучше шифровать
#                 )
#                 self.stdout.write(self.style.SUCCESS(f'Ключи созданы для пользователя {user.username}'))
#             else:
#                 self.stdout.write(f'Ключи уже существуют для {user.username}')

