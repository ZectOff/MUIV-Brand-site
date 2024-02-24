from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['This will be', 'information section', 'but now it is just text'],
        'goods': ['Prod1', 'Prod2', 'Prod3',
                  'Prod4', 'Prod5', 'Prod6',
                  'Prod7', 'Prod8',
                 ]
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')

def category(request):
    return render(request, 'main/category.html')

def contacts(request):
    return render(request, 'main/contacts.html')
