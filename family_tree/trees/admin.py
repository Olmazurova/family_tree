from django.contrib import admin

from .models import Tree, Person

admin.site.empty_value_display = 'Отсутствует'


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    """Класс администрирования древа."""

    list_display = (
        'genus_name',
        'created_at',
        'changed_at',
        'info',
        # 'linked_tree', # как в админке отобразить поля M:N?
        'owner',
        'is_public',
        'slug'
    )
    list_editable = (
        'is_public',
    )
    list_filter = (
        'genus_name',
        'created_at',
        'changed_at',
        'owner',
        'is_public',
    )
    list_display_links = (
        'genus_name',
        'info',
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Класс администрирования человека."""

    list_display = (
        # 'genus_name', # как в админке отобразить поля M:N?
        'surname',
        'name',
        'maiden_name',
        'patronymic',
        'birthday',
        'date_of_death',
        'gender',
        # 'biography',
        'photo',
        # 'parents',
        'spouse',
        # 'child',
    )
    list_filter = (
        # 'genus_name',
        'surname',
        'name',
        'maiden_name',
        'birthday',
        'date_of_death',
        'gender',
    )
    list_display_links = (
        # 'genus_name',
        'surname',
        'name',
        'maiden_name',
        'patronymic',
        'birthday',
        'date_of_death',
        'gender',
        # 'biography',
    )


