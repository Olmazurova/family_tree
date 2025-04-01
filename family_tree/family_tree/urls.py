"""
URL configuration for family_tree project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls import handler400
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from trees.views import HomeView
from users.views import UserCreate
from pages.views import RulesView

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Пути для работы с пользователями
urlpatterns += [
    path('user/', include('django.contrib.auth.urls')),
    path('user/registration', UserCreate.as_view(), name='registration'),
]

# Кастомные пути
urlpatterns += [
    path('home/', HomeView.as_view(), name='home'),
    path('profile/', include('users.urls')),
    path('tree/', include('trees.urls')),
    path('rules/', RulesView.as_view(), name='rules'),
    path('', HomeView.as_view(), name='home'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
handler403 = 'pages.views.csrf_failure'

# Подключаем функцию static() к urlpatterns:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)