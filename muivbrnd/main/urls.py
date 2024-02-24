from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('category', views.category, name='category'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
]
