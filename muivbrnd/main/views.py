from django.shortcuts import render

from recommendations.services import build_homepage_context


def index(request):
    context = {
        "title": "MUIV Brand - Главная страница",
        "values": ["This will be", "information section", "but now it is just text"],
        "instruction": [1, 2, 3, 4],
        **build_homepage_context(request.user),
    }
    return render(request, "main/index.html", context)


def about(request):
    about_data = {
        "title": "MUIV Brand - О компании",
        "bclabel": ["Главная", "О компании"],
    }
    return render(request, "main/about.html", about_data)


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
    from recommendations.services import (
        build_homepage_context,
        get_random_products,
        get_scroll_products,
    )

    testing_data = {
        "title": "MUIV Brand - Тестирование и отладка",
        "products": get_random_products(100),
        **build_homepage_context(request.user),
        "bclabel": ["Главная", "Тестирование приложения"],
    }
    testing_data["scroll_prds"] = get_scroll_products()
    return render(request, "main/testing.html", testing_data)
