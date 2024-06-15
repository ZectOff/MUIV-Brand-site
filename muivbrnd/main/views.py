from django.db.models import Prefetch
from django.shortcuts import render
import random as rnd

from goods.models import Products
from orders.models import Order, OrderItem


products_list = Products.objects.all()
prod_cloth = products_list.filter(category=2)
prod_access = products_list.filter(category=3)
prod_kanc = products_list.filter(category=4)

pepe1 = products_list.filter(id=13)
pepe2 = products_list.filter(id=34)
pepe3 = products_list.filter(id=10)
pepe4 = products_list.filter(id=14)

# При восстановлении БД, данные переменные закоментить,
# тк они пытаються отобрать элементы от бэйсменеджера,
# но без миграций и дампа они будут пустые и будут мешать.
sc_prd1 = pepe1[0]
sc_prd2 = pepe2[0]
sc_prd3 = pepe3[0]
sc_prd4 = pepe4[0]

def index(request):

    prd_pop_cloth = rnd.sample(list(prod_cloth), 4)
    prd_pop_kanc = rnd.sample(list(prod_kanc), 4)
    prd_pop_access = rnd.sample(list(prod_access), 4)

    if request.user.is_authenticated:
        is_orders = Order.objects.filter(user=request.user)
        orders = Order.objects.filter(user=request.user).prefetch_related(
                    Prefetch(
                        "orderitem_set",
                        queryset=OrderItem.objects.select_related("product"),
                    )
                ).order_by("-id")
        if is_orders:
            rec_cat_id = []
            rec_cat_name = []
            rec_cat_slug = []
            topcat_id_dict = {}
            topcat_name_dict = {}
            topcat_slug_dict = {}

            for order in orders:
                for item_o in order.orderitem_set.all():
                    rec_cat_id.append(item_o.product.category.id)
                    rec_cat_name.append(item_o.product.category.name)
                    rec_cat_slug.append(item_o.product.category.slug)

            for rc_id in rec_cat_id:
                if rc_id in topcat_id_dict:
                    topcat_id_dict[rc_id] += 1
                else: 
                    topcat_id_dict[rc_id] = 1

            topcat_id_1 = max(topcat_id_dict, key=topcat_id_dict.get)
            topcat_id_dict.pop(topcat_id_1)
            if topcat_id_dict:
                topcat_id_2 = max(topcat_id_dict, key=topcat_id_dict.get)
            else:
                topcat_id_2 = 2

            for rc_name in rec_cat_name:
                if rc_name in topcat_name_dict:
                    topcat_name_dict[rc_name] += 1
                else: 
                    topcat_name_dict[rc_name] = 1
                    
            topcat_name_1 = max(topcat_name_dict, key=topcat_name_dict.get)
            topcat_name_dict.pop(topcat_name_1)
            if topcat_name_dict:
                topcat_name_2 = max(topcat_name_dict, key=topcat_name_dict.get)
            else:
                topcat_name_2 = 'Одежда'

            for rc_slug in rec_cat_slug:
                if rc_slug in topcat_slug_dict:
                    topcat_slug_dict[rc_slug] += 1
                else: 
                    topcat_slug_dict[rc_slug] = 1

            topcat_slug_1 = max(topcat_slug_dict, key=topcat_slug_dict.get)
            topcat_slug_dict.pop(topcat_slug_1)
            if topcat_slug_dict:
                topcat_slug_2 = max(topcat_slug_dict, key=topcat_slug_dict.get)
            else:
                topcat_slug_2 = 'Odezhda'

            if topcat_id_1 == 2:
                rec_list_1 = prd_pop_cloth
            elif topcat_id_1 == 3:
                rec_list_1 = prd_pop_access
            elif topcat_id_1 == 4:
                rec_list_1 = prd_pop_kanc

            if topcat_id_2 == 2:
                rec_list_2 = prd_pop_cloth
            elif topcat_id_2 == 3:
                rec_list_2 = prd_pop_access
            elif topcat_id_2 == 4:
                rec_list_2 = prd_pop_kanc

        else:
            orders = None
            is_orders = None
            rec_list_1 = None
            rec_list_2 = None
            topcat_name_1 = None
            topcat_name_2 = None
            topcat_id_1 = None
            topcat_id_2 = None
            topcat_slug_1 = None
            topcat_slug_2 = None
    else:
        orders = None
        is_orders = None
        rec_list_1 = None
        rec_list_2 = None
        topcat_name_1 = None
        topcat_name_2 = None
        topcat_id_1 = None
        topcat_id_2 = None
        topcat_slug_1 = None
        topcat_slug_2 = None

    prd_random_8 = rnd.sample(list(products_list), 8)
    scroll_prds = [sc_prd1, sc_prd2, sc_prd3, sc_prd4]

    data = {
        "title": "MUIV Brand - Главная страница",
        "values": ["This will be", "information section", "but now it is just text"],
        "instruction": [1, 2, 3, 4],
        "products_r8": prd_random_8,
        "products_pop_cloth": prd_pop_cloth,
        "products_pop_kanc": prd_pop_kanc,
        "is_orders": is_orders,
        "rec_list_1": rec_list_1,
        "rec_list_2": rec_list_2,
        "scroll_prds": scroll_prds,
        "topcat_name_1": topcat_name_1,
        "topcat_name_2": topcat_name_2,
        "topcat_slug_1": topcat_slug_1,
        "topcat_slug_2": topcat_slug_2,
    }
    return render(request, "main/index.html", data)


def about(request):

    about_data = {
        "title": "MUIV Brand - О компании",
        "bclabel": ["Главная", "О компании"],
    }
    return render(request, "main/about.html", about_data)

# Контроллеры для остальных приложений, которые будут добавлены позже


def news(request):

    posts = {
        "title": "MUIV Brand - Новости",
        "posts": ['The new update!', 'The new update!', 'The new update!', 'The new update!'],
    }
    return render(request, "main/news.html", posts)

def support(request):

    sup_data = {
        "title": "MUIV Brand - Тех. поддержка",
        "bclabel": ["Главная", "Поддержка"],
    }
    return render(request, "main/support.html", sup_data)


def testing(request):

    prd_random_8 = rnd.sample(list(products_list), 8)

    # prd_pop_canc = rnd.sample(list(p), 3)
    prd_pop_cloth = rnd.sample(list(prod_cloth), 4)
    prd_pop_kanc = rnd.sample(list(prod_kanc), 4)

    scroll_prds = [sc_prd1, sc_prd2, sc_prd3, sc_prd4]

    testing_data = {
        "title": "MUIV Brand - Тестирование и отладка",
        "products": products_list,
        "products_r8": prd_random_8,
        "products_pop_cloth": prd_pop_cloth,
        "products_pop_kanc": prd_pop_kanc,
        "bclabel": ["Главная", "Тестирование приложения"],
    }
    return render(request, "main/testing.html", testing_data)
