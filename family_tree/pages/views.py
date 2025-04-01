from django.shortcuts import render
from django.views.generic import TemplateView


class RulesView(TemplateView):
    """Представление страницы правил проекта 'древо Рода'"""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Представление страницы ошибки 404."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Представление страницы ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Представление страницы ошибки 500."""
    return render(request, 'pages/500.html', status=500)


