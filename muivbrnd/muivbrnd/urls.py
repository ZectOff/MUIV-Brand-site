"""
URL configuration for muivbrnd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from muivbrnd import settings
from analytics import views
from main import views as main_views

admin.site.site_header = 'MUIV Brand — панель управления'
admin.site.site_title = 'MUIV Brand'
admin.site.index_title = 'Управление магазином'

urlpatterns = [
    path('admin/analytics/', admin.site.admin_view(views.dashboard), name='analytics_dashboard'),
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('catalog/', include('goods.urls', namespace='catalog')),
    path('user/', include('users.urls', namespace='user')),
    path('cart/', include('carts.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

# Статика и медиа для локального runserver (в т.ч. DEBUG=False)
urlpatterns += [
    re_path(
        r'^static/(?P<path>.*)$',
        serve,
        {'document_root': settings.STATICFILES_DIRS[0]},
    ),
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]

handler404 = main_views.page_not_found


# www.site.com/admin
# www.site.com
# www.site.com/about
# www.site.com/catalog
# www.site.com/catalog/product
