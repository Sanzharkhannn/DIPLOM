# choose/signals.py
import base64
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from Crypto.PublicKey import RSA  # type: ignore
from choose.models import UserRSAKeys, Content
from choose.crypto import encrypt_privkey

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_rsa_keys(sender, instance: User, created: bool, **kwargs):
    """
    При создании нового пользователя — создаём ему пару ключей,
    шифруем приватный ключ и сохраняем в UserRSAKeys.
    """
    if not created:
        return

    # если вдруг уже есть — ничего не делаем
    if UserRSAKeys.objects.filter(user=instance).exists():
        return

    # генерируем пару
    key = RSA.generate(2048)
    priv_pem = key.export_key(format='PEM')        # bytes
    pub_pem  = key.publickey().export_key(format='PEM')

    # шифруем приватный ключ
    encrypted_priv = encrypt_privkey(priv_pem)

    UserRSAKeys.objects.create(
        user=instance,
        public_key=pub_pem.decode('utf-8'),
        private_key_encrypted=encrypted_priv
    )


@receiver(post_save, sender=Content)
def fill_content_keys(sender, instance: Content, created: bool, **kwargs):
    """
    При создании нового Content — заполняем у него public/private_key из UserRSAKeys.
    """
    if not created:
        return

    # если у контента уже есть ключи — ничего не делаем
    if instance.public_key and instance.private_key_encrypted:
        return

    try:
        user_keys = UserRSAKeys.objects.get(user=instance.user)
    except UserRSAKeys.DoesNotExist:
        # можно залогировать или уведомить администратора
        return

    instance.public_key            = user_keys.public_key
    instance.private_key_encrypted = user_keys.private_key_encrypted
    # сохраняем один SQL-апдейт
    instance.save(update_fields=['public_key', 'private_key_encrypted'])