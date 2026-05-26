from django.urls import path
from goods import views

app_name = 'goods'

urlpatterns = [
    path('search', views.catalog, name='search'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/toggle/', views.favorite_toggle, name='favorite_toggle'),
    path('<slug:category_slug>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]
