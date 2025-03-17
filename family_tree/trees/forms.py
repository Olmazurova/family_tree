from django import forms

from .models import Tree, Person


class TreeForm(forms.ModelForm):
    """Форма древа на основе модели древа."""

    class Meta:
        model = Tree
        exclude = (
            'created_at',
            'changed_at',
            'owner',
        )


class PersonForm(forms.ModelForm):
    """Форма описания человека на основе модели описания человека."""

    class Meta:
        model = Person
        fields = (
            'genus_name',
            'surname',
            'name',
            'maiden_name',
            'patronymic',
            'birthday',
            'date_of_death',
            'gender',
            'biography',
            'photo',
            'father',
            'mother',
            'spouse',
            'child',
        )
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
        }