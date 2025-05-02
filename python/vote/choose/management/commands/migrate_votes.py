# choose/management/commands/migrate_votes.py
import base64
from django.core.management.base import BaseCommand
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from choose.models import ContentOptionVote, EncryptedVote

class Command(BaseCommand):
    help = "Миграция старых голосов ContentOptionVote → EncryptedVote"

    def handle(self, *args, **opts):
        qs = ContentOptionVote.objects.select_related('option__content')
        total = qs.count()
        self.stdout.write(f"Найдено {total} старых голосов...")

        for old_vote in qs:
            content = old_vote.option.content
            # загружаем публичный ключ опроса
            pubkey = serialization.load_pem_public_key(
                content.public_key.encode()
            )
            # шифруем идентификатор опции (или option_text)
            pt = str(old_vote.option.id).encode()  # можно option_text.encode()
            ct = pubkey.encrypt(
                pt,
                padding.OAEP(
                    mgf=padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            b64 = base64.b64encode(ct).decode()

            # создаём зашифрованный голос
            EncryptedVote.objects.create(
                content=content,
                encrypted_choice=b64,
                voted_at=old_vote.voted_at
            )
            self.stdout.write(f"✓ Голос #{old_vote.id} мигрирован")

        # после успешного переноса можно удалить старые
        deleted, _ = ContentOptionVote.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            f"Удалено {deleted} записей ContentOptionVote"
        ))
        self.stdout.write(self.style.SUCCESS("Миграция завершена."))