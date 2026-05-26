from django import template
from django.utils.html import format_html
from django.utils.http import urlencode

from goods.models import Categories
from goods.product_media import category_placeholder_icon, product_has_image
from goods.services import is_product_favorite

register = template.Library()


@register.filter
def has_product_image(product):
    return product_has_image(product)


@register.filter
def is_favorite_product(user, product):
    return is_product_favorite(user, product)


@register.simple_tag
def product_category_icon(product):
    category = getattr(product, 'category', None)
    return category_placeholder_icon(category)


@register.simple_tag()
def tag_categories():
    return Categories.objects.all()


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.simple_tag
def star_rating(rating, show_value=True):
    """
    Рендер звёзд рейтинга без inclusion_tag — обход бага копирования
    Context на Python 3.14 + Django 5.0 (super/dicts).
    """
    if rating is None:
        value = 0.0
        full_stars = 0
        has_rating = False
    else:
        value = float(rating)
        full_stars = min(5, max(0, int(round(value))))
        has_rating = True

    stars = format_html(
        '<span class="product-stars" aria-label="Оценка {} из 5">',
        f'{value:.1f}' if has_rating else 'нет',
    )
    for i in range(1, 6):
        if i <= full_stars:
            stars += format_html(
                '<span class="benk product-star-filled">&#9733;</span>'
            )
        else:
            stars += format_html(
                '<span class="product-star-empty">&#9734;</span>'
            )
    stars += format_html('</span>')

    if show_value and has_rating:
        stars += format_html(
            '<span class="product-rating-value">{}</span>',
            f'{value:.1f}',
        )
    return stars
