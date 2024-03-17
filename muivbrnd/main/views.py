from django.shortcuts import render
from django.http import HttpResponse

from goods.models import Categories

def index(request):

    categories = Categories.objects.all()

    data = {
        'title': 'MUIV Brand - Главная страница',
        'values': ['This will be', 'information section', 'but now it is just text'],
        'goods': ['Product_1', 'Product_2', 'Product_3',
                  'Product_4', 'Product_5', 'Product_6',
                  'Product_7', 'Product_8',
                 ],
        'instruction': ['Действие_1', 'Действие_2', 'Действиe_3',
                        'Действие_4', 
                ],
        'categories': categories
    }
    return render(request, 'main/index.html', data)

def about(request):
    categories = Categories.objects.all()

    about_data = {
        'title': 'MUIV Brand - О компании',
        'categories': categories,
        'bclabel': ['Главная', 'О компании']
    }
    return render(request, 'main/about.html', about_data)

def category(request):
    return render(request, 'main/category.html')

def contacts(request):
    return render(request, 'main/contacts.html')

# Контроллеры для остальных приложений, которые будут добавлены позже

def news(request):

    categories = Categories.objects.all()

    posts = {
        'title': 'MUIV Brand - Новости',
        'posts': ['Новость_1', 'Новость_2', 'Новость_3', 'Новость_4', 'Новость_5'],
        'post_content': ['Текст новости 1', 'Текст новости 2', 'Текст новости 3',
                         'Текст новости 4', 'Текст новости 5',],
        'comments': ['Я думаю это крутая идея!', 'Ребят эта топчик, поддерживаю вас'],
        'categories': categories
    }
    return render(request, 'main/news.html', posts)

def account(request):

    categories = Categories.objects.all()

    account_data = {
        'title': 'MUIV Brand - Аккаунт',
        'categories': categories
    }
    return render(request, 'main/account.html', account_data)

def login(request):

    categories = Categories.objects.all()

    login_data = {
        'title': 'MUIV Brand - Авторизация',
        'categories': categories,
        'bclabel': ['Главная', 'Авторизация', 'Вход']
    }
    return render(request, 'main/login.html', login_data)

def register(request):

    categories = Categories.objects.all()

    reg_data = {
        'title': 'MUIV Brand - Регистрация',
        'categories': categories,
        'bclabel': ['Главная', 'Авторизация', 'Вход']
    }
    return render(request, 'main/register.html', reg_data)

def support(request):

    categories = Categories.objects.all()

    sup_data = {
        'title': 'MUIV Brand - Тех. поддержка',
        'categories': categories,
        'bclabel': ['Главная', 'Поддержка']
    }
    return render(request, 'main/support.html', sup_data)