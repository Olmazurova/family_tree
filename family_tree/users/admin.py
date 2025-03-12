from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FamilyTreeUser

# Добавляем дополнительные поля к стандартной форме редактирования пользователя
UserAdmin.fieldsets += (
    ("Extra Fields", {"fields": ("about_oneself", "birthday", "photo",)}),
)

admin.site.register(FamilyTreeUser, UserAdmin)
