import os
from django.core.management.base import BaseCommand
from choose.models import UserRSAKeys
from choose.crypto import encrypt_privkey

class Command(BaseCommand):
    help = "Разовая команда: шифрует все голые private_key_encrypted в UserRSAKeys"

    def handle(self, *args, **options):
        # Проверяем, что мастер-ключ в окружении есть
        if not os.environ.get("MASTER_KEY"):
            self.stderr.write(self.style.ERROR(
                "MASTER_KEY не задан в окружении. "
                "Перед запуском: export MASTER_KEY=ваш_ключ"
            ))
            return

        qs = UserRSAKeys.objects.all()
        for uk in qs:
            raw = uk.private_key_encrypted  # сейчас здесь лежит чистый PEM
            # простая эвристика: начинаются ли данные с PEM-хедера?
            if raw.strip().startswith("-----BEGIN"):
                encrypted = encrypt_privkey(raw.encode())
                uk.private_key_encrypted = encrypted
                uk.save(update_fields=["private_key_encrypted"])
                self.stdout.write(self.style.SUCCESS(
                    f"{uk.user.username}: приватник зашифрован"
                ))
            else:
                self.stdout.write(
                    f"{uk.user.username}: похоже, уже зашифровано, пропускаем"
                )
        self.stdout.write(self.style.NOTICE("Готово"))