from django import forms
from django.shortcuts import get_object_or_404

from .models import Tree


WIDGET_SETTINGS = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


def get_tree(obj):
    return get_object_or_404(Tree, slug=obj.kwargs.get('slug'))


def form_valid_base(form):
    new_person = form.instance
    new_person.save()

    if new_person.spouse:
        spouse = new_person.spouse
        spouse.spouse = new_person
        spouse.save()

    return new_person
