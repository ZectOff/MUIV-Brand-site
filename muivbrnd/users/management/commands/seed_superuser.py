from django.core.management.base import BaseCommand

from users.seed_helpers import ADMIN_PASSWORD, ADMIN_USERNAME, ensure_admin_superuser


class Command(BaseCommand):
    help = (
        'Создаёт суперпользователя admin с паролем root '
        '(полный доступ к /admin/).'
    )

    def handle(self, *args, **options):
        user, created = ensure_admin_superuser()
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Создан суперпользователь {ADMIN_USERNAME} / {ADMIN_PASSWORD}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Суперпользователь {ADMIN_USERNAME} обновлён '
                    f'(пароль: {ADMIN_PASSWORD}, staff + superuser)'
                )
            )
