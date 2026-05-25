from django.db.models import Avg, Count

from goods.models import ProductReview, Products
from orders.models import OrderItem


def user_has_purchased_product(user, product):
    if not user or not user.is_authenticated:
        return False
    return OrderItem.objects.filter(
        order__user=user,
        product=product,
    ).exists()


def user_can_add_review(user, product):
    if not user_has_purchased_product(user, product):
        return False
    return not ProductReview.objects.filter(user=user, product=product).exists()


def get_product_rating_stats(product):
    stats = ProductReview.objects.filter(product=product).aggregate(
        average=Avg('rating'),
        count=Count('id'),
    )
    count = stats['count'] or 0
    average = round(float(stats['average']), 1) if count else None
    return {
        'average': average,
        'count': count,
    }


def get_product_reviews(product):
    return (
        ProductReview.objects.filter(product=product)
        .select_related('user')
        .order_by('-rating', '-created_at')
    )
