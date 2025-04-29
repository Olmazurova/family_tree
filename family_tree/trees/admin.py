from django.contrib import admin

from .models import Tree, Person

admin.site.empty_value_display = 'Отсутствует'


class LinkedTreeInline(admin.TabularInline):
    """Класс для отражения в админке связанных родословных."""
    # не работает, говорит, что поля from_tree_id нет
    model = Tree.linked_tree.through
    fields = ('genus_name',)
    extra = 0
    fk_name = "from_tree_id"


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    """Класс администрирования древа."""

    list_display = (
        'genus_name',
        'created_at',
        'changed_at',
        'info',
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
    # inlines = (LinkedTreeInline,)  # не работает


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Класс администрирования человека."""

    list_display = (
        'surname',
        'name',
        'maiden_name',
        'patronymic',
        'birthday',
        'date_of_death',
        'gender',
        'photo',
        'spouse',
    )
    list_filter = (
        'surname',
        'name',
        'maiden_name',
        'birthday',
        'date_of_death',
        'gender',
    )
    list_display_links = (
        'surname',
        'name',
        'maiden_name',
        'patronymic',
        'birthday',
        'date_of_death',
        'gender',
    )
