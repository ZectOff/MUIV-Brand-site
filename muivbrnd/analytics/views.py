from django.contrib import admin
from django.shortcuts import render

from analytics.services import build_dashboard_context


def dashboard(request):
    period = request.GET.get('period')
    context = {
        **admin.site.each_context(request),
        **build_dashboard_context(period),
        'title': 'Аналитика продаж',
    }
    return render(request, 'analytics/dashboard.html', context)
