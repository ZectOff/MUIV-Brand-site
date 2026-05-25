from django.contrib import admin
from django.shortcuts import render

from analytics.services import build_dashboard_context


def dashboard(request):
    context = {
        **admin.site.each_context(request),
        **build_dashboard_context(),
        'title': 'Аналитика продаж',
    }
    return render(request, 'analytics/dashboard.html', context)
