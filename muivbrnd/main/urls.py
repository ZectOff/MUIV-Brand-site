from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('category', views.category, name='category'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('news', views.news, name='news'),
    path('account', views.account, name='account'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('support', views.support, name='support'),
]
