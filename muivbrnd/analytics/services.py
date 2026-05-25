from datetime import timedelta

from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncDate
from django.utils import timezone

from orders.models import Order, OrderItem


def _line_total():
    return ExpressionWrapper(
        F('price') * F('quantity'),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )


def get_summary():
    items = OrderItem.objects.all()
    orders = Order.objects.all()

    revenue = items.aggregate(
        total=Sum(_line_total())
    )['total'] or 0

    total_qty = items.aggregate(total=Sum('quantity'))['total'] or 0
    orders_count = orders.count()

    avg_order = round(float(revenue) / orders_count, 2) if orders_count else 0

    return {
        'orders_count': orders_count,
        'items_sold': total_qty,
        'revenue': float(revenue),
        'avg_order': avg_order,
    }


def get_top_products(limit=10):
    rows = (
        OrderItem.objects
        .values('name', 'product__category__name')
        .annotate(
            total_qty=Sum('quantity'),
            total_revenue=Sum(_line_total()),
        )
        .order_by('-total_qty')[:limit]
    )
    return [
        {
            'name': row['name'],
            'category': row['product__category__name'] or '—',
            'quantity': row['total_qty'],
            'revenue': float(row['total_revenue'] or 0),
        }
        for row in rows
    ]


def get_top_categories(limit=8):
    rows = (
        OrderItem.objects
        .filter(product__isnull=False)
        .values('product__category__name')
        .annotate(
            total_qty=Sum('quantity'),
            total_revenue=Sum(_line_total()),
        )
        .order_by('-total_qty')[:limit]
    )
    return [
        {
            'name': row['product__category__name'] or 'Без категории',
            'quantity': row['total_qty'],
            'revenue': float(row['total_revenue'] or 0),
        }
        for row in rows
    ]


def get_orders_timeline(days=30):
    since = timezone.now() - timedelta(days=days)
    rows = (
        OrderItem.objects
        .filter(order__created_timestamp__gte=since)
        .annotate(day=TruncDate('order__created_timestamp'))
        .values('day')
        .annotate(
            orders_count=Count('order', distinct=True),
            items_count=Sum('quantity'),
            revenue=Sum(_line_total()),
        )
        .order_by('day')
    )
    return [
        {
            'date': row['day'].strftime('%d.%m') if row['day'] else '',
            'orders': row['orders_count'],
            'items': row['items_count'] or 0,
            'revenue': float(row['revenue'] or 0),
        }
        for row in rows
    ]


def build_dashboard_context():
    return {
        'summary': get_summary(),
        'top_products': get_top_products(),
        'top_categories': get_top_categories(),
        'orders_timeline': get_orders_timeline(),
    }
