from django.core.management.base import BaseCommand
from choose.models import Content, EncryptedVote, PollResult, ContentOption
from choose.crypto import decrypt_privkey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64, os

class Command(BaseCommand):
    help = "Расшифровывает и считает голоса"

    def handle(self, *args, **options):
        # Проверяем, что есть доступ к MASTER_KEY
        if not os.environ.get("MASTER_KEY"):
            self.stderr.write("ERROR: MASTER_KEY is not set")
            return

        for poll in Content.objects.all():
            # 1) Расшифровываем приватный ключ опроса
            priv_pem = decrypt_privkey(poll.private_key_encrypted)
            priv_key = serialization.load_pem_private_key(priv_pem, password=None)

            # 2) Считаем зашифрованные голоса
            counts = {}  # ключами будут option_text
            for v in EncryptedVote.objects.filter(content=poll):
            # 1) base64 → cipher bytes
                ct = base64.b64decode(v.encrypted_choice)
                # 2) rsa decrypt → получится строка с id варианта, например "5"
                pt = priv_key.decrypt(
                    ct,
                    padding.OAEP(
                        mgf=padding.MGF1(hashes.SHA256()),
                        algorithm=hashes.SHA256(), 
                        label=None
                    )
                ).decode()
                try:
                    opt_id = int(pt)
                    opt = ContentOption.objects.get(pk=opt_id)
                    label = opt.option_text
                except (ValueError, ContentOption.DoesNotExist):
                    # на всякий случай fallback
                    label = f"Unknown option #{pt}"

                counts[label] = counts.get(label, 0) + 1

            # 3) записываем в PollResult
            PollResult.objects.filter(content=poll).delete()
            for label, cnt in counts.items():
                PollResult.objects.create(
                    content=poll,
                    option_text=label,
                    votes=cnt
                )
                self.stdout.write(f"Poll {poll.id!r}: saved {len(counts)} result rows")



# from django.core.management.base import BaseCommand
# from choose.models import Content, EncryptedVote
# from choose.crypto import decrypt_privkey
# from cryptography.hazmat.primitives import serialization, hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# import base64, os

# class Command(BaseCommand):
#     help = "Расшифровывает и считает голоса"

#     def handle(self, *args, **options):
#         # проверяем, что есть MASTER_KEY
#         if not os.environ.get("MASTER_KEY"):
#             self.stderr.write("MASTER_KEY не задан")
#             return

#         for content in Content.objects.all():
#             print(f"Подсчет для опроса «{content.title}»")
#             # раскодируем приватный PEM
#             priv_pem = decrypt_privkey(content.private_key_encrypted)
#             priv = serialization.load_pem_private_key(priv_pem, password=None)

#             counts = {}
#             for v in EncryptedVote.objects.filter(content=content):
#                 ct = base64.b64decode(v.encrypted_choice)
#                 pt = priv.decrypt(
#                     ct,
#                     padding.OAEP(
#                         mgf=padding.MGF1(hashes.SHA256()),
#                         algorithm=hashes.SHA256(), label=None
#                     )
#                 ).decode()
#                 counts[pt] = counts.get(pt, 0) + 1

#             for opt, cnt in counts.items():
#                 print(f"  {opt}: {cnt}")
#             print("-" * 30)