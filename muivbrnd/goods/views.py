from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.models import Products
from goods.utils import q_search
# import random as rnd


def catalog(request, category_slug=None):

    # prd_list = Products.objects.all()
    # length_ofp = len(prd_list)

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == "vse-tovary":
        # goods = rnd.sample(list(prd_list), length_ofp)
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 12)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Категории',
        'products': current_page,
        'slug_url': category_slug
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):

    get_prd = Products.objects.get(slug=product_slug)

    prd_data = {
        'title': 'MUIV Brand - Карта товара ',
        'catgoods': ['Img-1', 'Img-2', 'Img-3',],
        'product': get_prd
    }
    return render(request, 'goods/product.html', context=prd_data)
