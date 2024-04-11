from django.shortcuts import render

from goods.models import Products
import random as rnd

products_list = Products.objects.all()



def catalog(request):

    length_ofp = len(products_list)
    products_all_cat = rnd.sample(list(products_list), length_ofp)

    data = {
        'title': 'Категории',
        'products': products_list,
        'rnd_products': products_all_cat
    }
    return render(request, 'goods/catalog.html', context=data)

def product(request, product_slug):

    get_prd = Products.objects.get(slug=product_slug)

    prd_data = {
        'title': 'MUIV Brand - Карта товара ',
        'catgoods': ['Img-1', 'Img-2', 'Img-3',],
        'product': get_prd
    }
    return render(request, 'goods/product.html', context=prd_data)
