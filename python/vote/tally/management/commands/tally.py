from django.core.management.base import BaseCommand
from choose.models import Content, EncryptedVote
from choose.crypto import decrypt_privkey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64, os

class Command(BaseCommand):
    help = "Расшифровывает и считает голоса"

    def handle(self, *args, **options):
        # проверяем, что есть MASTER_KEY
        if not os.environ.get("MASTER_KEY"):
            self.stderr.write("MASTER_KEY не задан")
            return

        for content in Content.objects.all():
            print(f"Подсчет для опроса «{content.title}»")
            # раскодируем приватный PEM
            priv_pem = decrypt_privkey(content.private_key_encrypted)
            priv = serialization.load_pem_private_key(priv_pem, password=None)

            counts = {}
            for v in EncryptedVote.objects.filter(content=content):
                ct = base64.b64decode(v.encrypted_choice)
                pt = priv.decrypt(
                    ct,
                    padding.OAEP(
                        mgf=padding.MGF1(hashes.SHA256()),
                        algorithm=hashes.SHA256(), label=None
                    )
                ).decode()
                counts[pt] = counts.get(pt, 0) + 1

            for opt, cnt in counts.items():
                print(f"  {opt}: {cnt}")
            print("-" * 30)