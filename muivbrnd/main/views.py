from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['This will be', 'information section', 'but now it is just text'],
        'goods': ['Product_1', 'Product_2', 'Product_3',
                  'Product_4', 'Product_5', 'Product_6',
                  'Product_7', 'Product_8',
                 ],
        'instruction': ['Действие_1', 'Действие_2', 'Действи_3',
                        'Действие_4', 
                ],
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')

def category(request):
    return render(request, 'main/category.html')

def contacts(request):
    return render(request, 'main/contacts.html')
