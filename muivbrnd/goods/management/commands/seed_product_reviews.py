import random

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from goods.models import ProductReview, Products
from orders.models import Order, OrderItem

User = get_user_model()

REVIEWER_PROFILES = [
    ('reviewer_anna', 'Анна', 'Козлова', '79101110001'),
    ('reviewer_ivan', 'Иван', 'Петров', '79102220002'),
    ('reviewer_maria', 'Мария', 'Сидорова', '79103330003'),
    ('reviewer_dmitry', 'Дмитрий', 'Волков', '79104440004'),
    ('reviewer_elena', 'Елена', 'Морозова', '79105550005'),
    ('reviewer_alexey', 'Алексей', 'Новиков', '79106660006'),
    ('reviewer_olga', 'Ольга', 'Фёдорова', '79107770007'),
    ('reviewer_sergey', 'Сергей', 'Кузнецов', '79108880008'),
    ('reviewer_natalia', 'Наталья', 'Попова', '79109990009'),
    ('reviewer_pavel', 'Павел', 'Соколов', '79101010010'),
    ('reviewer_irina', 'Ирина', 'Лебедева', '79101110111'),
    ('reviewer_mikhail', 'Михаил', 'Козлов', '79101220222'),
]

REVIEW_TEXTS = {
    5: [
        'Отличный товар, качество на высоте! Рекомендую.',
        'Очень доволен покупкой, всё как на сайте.',
        'Превзошло ожидания, буду заказывать ещё.',
        'Идеально подошло, спасибо MUIV Brand!',
    ],
    4: [
        'Хороший товар, небольшие мелочи, но в целом отлично.',
        'Качество радует, доставка быстрая.',
        'Понравилось, только хотелось бы чуть больше размеров.',
        'Достойная покупка за свои деньги.',
    ],
    3: [
        'Нормально, без восторга, но пользоваться можно.',
        'Средне: ожидал чуть лучше по материалу.',
        'Неплохо, но есть куда расти.',
    ],
    2: [
        'Сойдёт, но ожидал большего за эту цену.',
        'Есть недочёты, надеюсь улучшат.',
    ],
    1: [
        'Не совпало с ожиданиями, разочарован.',
    ],
}


def _get_or_create_reviewer(username, first_name, last_name, phone):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@reviews.local',
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone[:10],
        },
    )
    if created:
        user.set_password('testpass123')
        user.save(update_fields=['password'])
    return user


def _ensure_purchase(user, product):
    if OrderItem.objects.filter(order__user=user, product=product).exists():
        return False

    if product.quantity < 1:
        product.quantity = 1
        product.save(update_fields=['quantity'])

    order = Order.objects.create(
        user=user,
        phone_number=user.phone_number or '79000000000',
        requires_delivery=False,
        delivery_address='',
        payment_on_get=True,
        is_paid=True,
        status='Выполнен',
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        name=product.name,
        price=product.sell_price(),
        quantity=1,
    )
    if product.quantity > 0:
        product.quantity -= 1
        product.save(update_fields=['quantity'])
    return True


class Command(BaseCommand):
    help = (
        'Создаёт демо-отзывы для случайных товаров от разных пользователей '
        '(1–3 отзыва на товар, при необходимости — заказы).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--products',
            type=int,
            default=0,
            help='Сколько случайных товаров выбрать (0 = от 4 до 8).',
        )

    def handle(self, *args, **options):
        call_command('seed_superuser')

        products_qs = Products.objects.exclude(slug__isnull=True).exclude(slug='')
        products = list(products_qs)
        if not products:
            self.stderr.write(self.style.ERROR('В каталоге нет товаров.'))
            return

        count = options['products']
        if count <= 0:
            count = random.randint(4, min(8, len(products)))
        count = min(count, len(products))
        picked_products = random.sample(products, k=count)

        reviewers = [
            _get_or_create_reviewer(*profile) for profile in REVIEWER_PROFILES
        ]
        random.shuffle(reviewers)

        summary = []
        created_reviews = 0
        created_orders = 0

        for product in picked_products:
            review_count = random.randint(1, 3)
            available = [u for u in reviewers if not ProductReview.objects.filter(
                user=u, product=product
            ).exists()]
            if len(available) < review_count:
                available = reviewers[:]
            chosen_users = random.sample(available, k=min(review_count, len(available)))

            product_lines = []
            for user in chosen_users:
                if ProductReview.objects.filter(user=user, product=product).exists():
                    continue

                with transaction.atomic():
                    if _ensure_purchase(user, product):
                        created_orders += 1

                    rating = random.choices(
                        population=[5, 4, 4, 5, 3, 4, 5],
                        k=1,
                    )[0]
                    text = random.choice(REVIEW_TEXTS[rating])
                    ProductReview.objects.create(
                        user=user,
                        product=product,
                        rating=rating,
                        text=text,
                    )
                    created_reviews += 1
                    preview = text if len(text) <= 55 else f'{text[:55]}…'
                    product_lines.append(
                        f'  • {user.first_name} {user.last_name} ({user.username}) — '
                        f'оценка {rating}/5: {preview}'
                    )

            summary.append((product, review_count, product_lines))

        self.stdout.write(self.style.SUCCESS(
            f'\nСоздано отзывов: {created_reviews}, новых заказов: {created_orders}\n'
        ))
        self.stdout.write(self.style.MIGRATE_HEADING('Товары с отзывами:'))
        for product, planned, lines in summary:
            self.stdout.write(
                f'\n— {product.name} (slug: {product.slug}), отзывов: {len(lines)}'
            )
            for line in lines:
                self.stdout.write(line)

        self.stdout.write(self.style.SUCCESS('\nГотово.'))
