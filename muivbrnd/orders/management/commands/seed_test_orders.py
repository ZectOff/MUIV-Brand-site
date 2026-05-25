import random

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from carts.models import Cart
from goods.models import Products
from orders.models import Order, OrderItem

User = get_user_model()


class Command(BaseCommand):
    help = (
        'Создаёт суперпользователя admin/root и 10 тестовых пользователей '
        'с корзинами и заказами для аналитики'
    )

    def handle(self, *args, **options):
        call_command('seed_superuser')

        for i in range(1, 11):
            products = list(
                Products.objects.filter(quantity__gt=0)
                .exclude(slug__isnull=True)
                .exclude(slug='')
            )
            if not products:
                self.stderr.write(f'Недостаточно товаров для User_Test_{i}.')
                continue

            username = f'User_Test_{i}'
            phone = f'90{i:08d}'[:10]

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username.lower()}@test.local',
                    'first_name': 'Тест',
                    'last_name': str(i),
                    'phone_number': phone,
                },
            )
            if created:
                user.set_password('testpass123')
                user.save(update_fields=['password'])

            Cart.objects.filter(user=user).delete()

            picked = random.sample(products, k=min(random.randint(1, 3), len(products)))

            with transaction.atomic():
                for product in picked:
                    qty = random.randint(1, min(3, product.quantity))
                    Cart.objects.create(user=user, product=product, quantity=qty)

                cart_items = list(Cart.objects.filter(user=user).select_related('product'))
                order = Order.objects.create(
                    user=user,
                    phone_number=phone,
                    requires_delivery=False,
                    delivery_address='',
                    payment_on_get=True,
                )

                for cart_item in cart_items:
                    product = cart_item.product
                    qty = cart_item.quantity
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        name=product.name,
                        price=product.sell_price(),
                        quantity=qty,
                    )
                    product.quantity -= qty
                    product.save(update_fields=['quantity'])

                Cart.objects.filter(user=user).delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f'{username}: заказ №{order.pk}, позиций — {len(cart_items)}'
                )
            )

        self.stdout.write(self.style.SUCCESS('Готово: 10 пользователей и заказов.'))
