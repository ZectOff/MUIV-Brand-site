from django.contrib.auth import get_user_model

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'root'
ADMIN_EMAIL = 'admin@muiv.local'


def ensure_admin_superuser():
    """
    Создаёт или восстанавливает суперпользователя admin/root для панели Django.
    Пароль и флаги staff/superuser обновляются при каждом вызове.
    """
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=ADMIN_USERNAME,
        defaults={
            'email': ADMIN_EMAIL,
            'is_staff': True,
            'is_superuser': True,
        },
    )
    user.email = ADMIN_EMAIL
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.set_password(ADMIN_PASSWORD)
    user.save()
    return user, created
