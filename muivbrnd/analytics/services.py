from calendar import monthrange
from datetime import timedelta

from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncDate, TruncHour, TruncMonth
from django.utils import timezone

from orders.models import Order, OrderItem

WEEKDAY_LABELS = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс')

MONTH_NAMES = (
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
)

TIMELINE_PERIODS = {
    'day': {
        'label': 'Последние 24 часа',
        'trunc': 'hour',
    },
    'week': {
        'label': 'Текущая неделя',
        'trunc': 'day',
    },
    'month': {
        'label': 'Текущий месяц',
        'trunc': 'day',
    },
    'year': {
        'label': 'Текущий год',
        'trunc': 'month',
    },
}

DEFAULT_TIMELINE_PERIOD = 'month'


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
        .filter(product__isnull=False)
        .exclude(product__slug__isnull=True)
        .exclude(product__slug='')
        .values('name', 'product__slug', 'product__category__name')
        .annotate(
            total_qty=Sum('quantity'),
            total_revenue=Sum(_line_total()),
        )
        .order_by('-total_qty')[:limit]
    )
    return [
        {
            'name': row['name'],
            'slug': row['product__slug'],
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


def _local_now():
    return timezone.localtime(timezone.now())


def _empty_point():
    return {'orders': 0, 'items': 0, 'revenue': 0.0}


def _timeline_bucket_specs(period):
    """Возвращает (ключ_слота, подпись_оси) для всего периода."""
    now = _local_now()

    if period == 'day':
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        specs = []
        for hour in range(24):
            dt = day_start + timedelta(hours=hour)
            specs.append((dt, dt.strftime('%H:%M')))
        return specs, day_start, 'hour'

    if period == 'week':
        week_start = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        specs = []
        for offset in range(7):
            dt = week_start + timedelta(days=offset)
            specs.append((dt.date(), WEEKDAY_LABELS[dt.weekday()]))
        return specs, week_start, 'day'

    if period == 'month':
        days_in_month = monthrange(now.year, now.month)[1]
        month_start = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        specs = []
        for day in range(1, days_in_month + 1):
            dt = month_start.replace(day=day)
            specs.append((dt.date(), dt.strftime('%d.%m')))
        return specs, month_start, 'day'

    year = now.year
    year_start = now.replace(
        month=1, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    specs = []
    for month in range(1, 13):
        dt = year_start.replace(month=month, day=1)
        specs.append(((year, month), f'{month:02d}.{year}'))
    return specs, year_start, 'month'


def _bucket_key_from_db(value, trunc):
    if value is None:
        return None
    if trunc == 'day':
        if hasattr(value, 'date') and callable(value.date):
            return timezone.localtime(value).date()
        return value
    if trunc == 'hour':
        if hasattr(value, 'hour'):
            local = timezone.localtime(value)
            return local.replace(minute=0, second=0, microsecond=0)
        return value
    if trunc == 'month':
        if hasattr(value, 'year') and hasattr(value, 'month') and not hasattr(value, 'day'):
            return (value.year, value.month)
        local = timezone.localtime(value)
        return (local.year, local.month)
    return value


def _fetch_timeline_aggregates(since, trunc):
    queryset = OrderItem.objects.filter(order__created_timestamp__gte=since)

    if trunc == 'hour':
        queryset = queryset.annotate(bucket=TruncHour('order__created_timestamp'))
    elif trunc == 'month':
        queryset = queryset.annotate(bucket=TruncMonth('order__created_timestamp'))
    else:
        queryset = queryset.annotate(bucket=TruncDate('order__created_timestamp'))

    rows = queryset.values('bucket').annotate(
        orders_count=Count('order', distinct=True),
        items_count=Sum('quantity'),
        revenue=Sum(_line_total()),
    )
    return {
        _bucket_key_from_db(row['bucket'], trunc): {
            'orders': row['orders_count'],
            'items': row['items_count'] or 0,
            'revenue': float(row['revenue'] or 0),
        }
        for row in rows
    }


def get_orders_timeline(period=DEFAULT_TIMELINE_PERIOD):
    period = resolve_timeline_period(period)
    specs, since, trunc = _timeline_bucket_specs(period)
    data_by_key = _fetch_timeline_aggregates(since, trunc)

    timeline = []
    for key, label in specs:
        point = data_by_key.get(key, _empty_point())
        timeline.append({
            'date': label,
            'orders': point['orders'],
            'items': point['items'],
            'revenue': point['revenue'],
        })
    return timeline


def resolve_timeline_period(period_key):
    if period_key in TIMELINE_PERIODS:
        return period_key
    return DEFAULT_TIMELINE_PERIOD


def timeline_period_label(period):
    label = TIMELINE_PERIODS[period]['label']
    today = timezone.localdate()
    if period == 'day':
        label = f'{label} (за {today:%d.%m.%Y})'
    elif period == 'month':
        label = f'{label} ({MONTH_NAMES[today.month - 1]} {today.year})'
    elif period == 'year':
        label = f'{label} ({today.year})'
    return label


def build_dashboard_context(period=None):
    period = resolve_timeline_period(period)
    return {
        'summary': get_summary(),
        'top_products': get_top_products(),
        'top_categories': get_top_categories(),
        'orders_timeline': get_orders_timeline(period),
        'timeline_period': period,
        'timeline_period_label': timeline_period_label(period),
        'timeline_periods': [
            {'key': key, 'label': TIMELINE_PERIODS[key]['label']}
            for key in ('day', 'week', 'month', 'year')
        ],
    }
