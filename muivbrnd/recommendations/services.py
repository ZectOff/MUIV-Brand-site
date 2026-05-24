"""
Сервис подбора товаров для главной страницы.

Алгоритм для авторизованных пользователей с историей заказов:
  1. Считаем частоту покупок по категориям (сумма quantity в OrderItem).
  2. Берём две самые популярные категории (2, 3, 4 — без «Все товары»).
  3. В каждой категории выбираем до 4 товаров в наличии со slug,
     по возможности исключая уже купленные.

Для гостей и пользователей без заказов — два блока по умолчанию
(одежда и канцелярия) со случайными товарами.
"""

from collections import Counter
from dataclasses import dataclass
from random import sample
from typing import Iterable, Optional

from goods.models import Categories, Products
from orders.models import OrderItem

from .constants import (
    DEFAULT_CATEGORY_BLOCKS,
    PRODUCTS_PER_BLOCK,
    RANDOM_PRODUCTS_COUNT,
    RECOMMENDATION_CATEGORY_IDS,
    SCROLL_PRODUCT_IDS,
)


@dataclass(frozen=True)
class RecommendationBlock:
    category_name: str
    category_slug: str
    products: tuple


def sellable_products(category_id: Optional[int] = None):
    """Товары, доступные для ссылок в каталоге (есть slug и остаток)."""
    qs = (
        Products.objects.filter(quantity__gt=0)
        .exclude(slug__isnull=True)
        .exclude(slug='')
        .select_related('category')
    )
    if category_id is not None:
        qs = qs.filter(category_id=category_id)
    return qs


def safe_sample(queryset, count: int, exclude_ids: Optional[Iterable[int]] = None) -> list:
    exclude_ids = set(exclude_ids or ())
    pool = [p for p in queryset if p.id not in exclude_ids]
    if not pool:
        return []
    return sample(pool, min(count, len(pool)))


def fill_products(category_id: int, count: int, exclude_ids: Optional[set] = None) -> list:
    exclude_ids = set(exclude_ids or ())
    selected = safe_sample(sellable_products(category_id), count, exclude_ids)
    if len(selected) < count:
        extra = safe_sample(
            sellable_products(category_id),
            count - len(selected),
            exclude_ids | {p.id for p in selected},
        )
        selected.extend(extra)
    return selected[:count]


def purchased_product_ids(user) -> set:
    if not user.is_authenticated:
        return set()
    return set(
        OrderItem.objects.filter(
            order__user=user,
            product_id__isnull=False,
        ).values_list('product_id', flat=True)
    )


def user_has_orders(user) -> bool:
    if not user.is_authenticated:
        return False
    return OrderItem.objects.filter(
        order__user=user,
        product__category_id__in=RECOMMENDATION_CATEGORY_IDS,
    ).exists()


def top_categories_from_orders(user, limit: int = 2) -> list[tuple[int, str, str]]:
    """Возвращает [(category_id, name, slug), ...] по убыванию популярности."""
    items = OrderItem.objects.filter(
        order__user=user,
        product__isnull=False,
        product__category_id__in=RECOMMENDATION_CATEGORY_IDS,
    ).select_related('product__category')

    counter: Counter[int] = Counter()
    meta: dict[int, tuple[str, str]] = {}
    for item in items:
        cat = item.product.category
        counter[cat.id] += item.quantity
        meta[cat.id] = (cat.name, cat.slug)

    return [
        (cat_id, meta[cat_id][0], meta[cat_id][1])
        for cat_id, _ in counter.most_common(limit)
        if cat_id in meta
    ]


def build_block(category_id: int, name: str, slug: str, exclude_ids: set) -> Optional[RecommendationBlock]:
    products = fill_products(category_id, PRODUCTS_PER_BLOCK, exclude_ids)
    if not products:
        return None
    return RecommendationBlock(name, slug, tuple(products))


def default_blocks() -> list[RecommendationBlock]:
    blocks = []
    for category_id, _slug in DEFAULT_CATEGORY_BLOCKS:
        try:
            cat = Categories.objects.get(pk=category_id)
        except Categories.DoesNotExist:
            continue
        block = build_block(category_id, cat.name, cat.slug, set())
        if block:
            blocks.append(block)
    return blocks


def personalized_blocks(user) -> list[RecommendationBlock]:
    purchased = purchased_product_ids(user)
    blocks = []
    used_slugs = set()

    for category_id, name, slug in top_categories_from_orders(user, limit=2):
        if slug in used_slugs:
            continue
        block = build_block(category_id, name, slug, purchased)
        if block and len(block.products) == PRODUCTS_PER_BLOCK:
            blocks.append(block)
            used_slugs.add(slug)

    return blocks


def merge_with_defaults(personalized: list[RecommendationBlock]) -> list[RecommendationBlock]:
    result = list(personalized)
    used_slugs = {b.category_slug for b in result}

    for block in default_blocks():
        if len(result) >= 2:
            break
        if block.category_slug not in used_slugs:
            result.append(block)
            used_slugs.add(block.category_slug)

    return result[:2]


def get_recommendation_blocks(user) -> tuple[list[RecommendationBlock], bool]:
    """
    Возвращает (blocks, is_personalized).
    Всегда старается отдать ровно 2 блока по 4 товара (если хватает данных в БД).
    """
    if user.is_authenticated and user_has_orders(user):
        personalized = personalized_blocks(user)
        blocks = merge_with_defaults(personalized)
        is_personalized = len(personalized) > 0
        return blocks, is_personalized

    return default_blocks()[:2], False


def get_random_products(count: int = RANDOM_PRODUCTS_COUNT) -> list:
    return safe_sample(sellable_products(), count)


def get_scroll_products() -> list:
    preferred = list(
        sellable_products().filter(id__in=SCROLL_PRODUCT_IDS)
    )
    order = {pid: idx for idx, pid in enumerate(SCROLL_PRODUCT_IDS)}
    preferred.sort(key=lambda p: order.get(p.id, 999))
    if len(preferred) >= 4:
        return preferred[:4]

    fallback = safe_sample(sellable_products(), 4)
    return fallback if fallback else list(sellable_products()[:4])


def get_default_catalog_slug() -> str:
    cat = (
        Categories.objects.exclude(pk=1)
        .exclude(slug__isnull=True)
        .exclude(slug='')
        .order_by('pk')
        .first()
    )
    return cat.slug if cat else 'odezhda'


def build_homepage_context(user) -> dict:
    blocks, is_personalized = get_recommendation_blocks(user)
    return {
        'recommendation_blocks': blocks,
        'use_personalized_recommendations': is_personalized,
        'products_r8': get_random_products(),
        'scroll_prds': get_scroll_products(),
        'default_catalog_slug': get_default_catalog_slug(),
        'is_orders': user_has_orders(user) if user.is_authenticated else False,
    }
