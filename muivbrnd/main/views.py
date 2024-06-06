from django.shortcuts import render
import random as rnd

from goods.models import Products


products_list = Products.objects.all()
prod_cloth = products_list.filter(category=2)
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

    prd_random_8 = rnd.sample(list(products_list), 8)

    # prd_pop_canc = rnd.sample(list(p), 3)
    prd_pop_cloth = rnd.sample(list(prod_cloth), 4)
    prd_pop_kanc = rnd.sample(list(prod_kanc), 4)

    scroll_prds = [sc_prd1, sc_prd2, sc_prd3, sc_prd4]

    data = {
        "title": "MUIV Brand - Главная страница",
        "values": ["This will be", "information section", "but now it is just text"],
        "instruction": [1, 2, 3, 4],
        "products_r8": prd_random_8,
        "products_pop_cloth": prd_pop_cloth,
        "products_pop_kanc": prd_pop_kanc,
        "scroll_prds": scroll_prds,
    }
    return render(request, "main/index.html", data)


def about(request):

    about_data = {
        "title": "MUIV Brand - О компании",
        "bclabel": ["Главная", "О компании"],
    }
    return render(request, "main/about.html", about_data)


def category(request):
    return render(request, "main/category.html")


def contacts(request):
    return render(request, "main/contacts.html")


# Контроллеры для остальных приложений, которые будут добавлены позже


def news(request):

    posts = {
        "title": "MUIV Brand - Новости",
        "posts": ["Новость_1", "Новость_2", "Новость_3", "Новость_4", "Новость_5"],
        "post_content": [
            "Текст новости 1",
            "Текст новости 2",
            "Текст новости 3",
            "Текст новости 4",
            "Текст новости 5",
        ],
        "comments": ["Я думаю это крутая идея!", "Ребят эта топчик, поддерживаю вас"],
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
