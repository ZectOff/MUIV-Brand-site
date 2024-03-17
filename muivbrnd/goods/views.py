from django.shortcuts import render

from goods.models import Categories


def catalog(request):
    categories = Categories.objects.all()

    data = {
        'title': 'Категории',
        'catgoods': ['Product_1', 'Product_2', 'Product_3',
                     'Product_4', 'Product_5', 'Product_6',
                     'Product_7', 'Product_8', 'Product_9',
                     'Product_10', 'Product_11', 'Product_12',],
        'categories': categories
    }
    return render(request, 'goods/catalog.html', data)

def product(request):
    categories = Categories.objects.all()

    prd_data = {
        'title': 'MUIV Brand - Карта товара Prd1',
        'catgoods': ['Img-1', 'Img-2', 'Img-3',],
        'categories': categories
    }
    return render(request, 'goods/product.html', prd_data)
