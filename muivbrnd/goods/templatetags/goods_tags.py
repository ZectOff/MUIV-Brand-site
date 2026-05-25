from django import template
from django.utils.http import urlencode

from goods.models import Categories

register = template.Library()

@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.inclusion_tag('goods/includes/star_rating.html')
def star_rating(rating, show_value=True):
    if rating is None:
        return {
            'rating_value': 0.0,
            'full_stars': 0,
            'empty_stars': 5,
            'show_value': show_value,
            'has_rating': False,
        }
    value = float(rating)
    full_stars = min(5, max(0, int(round(value))))
    return {
        'rating_value': value,
        'full_stars': full_stars,
        'empty_stars': 5 - full_stars,
        'show_value': show_value,
        'has_rating': True,
    }