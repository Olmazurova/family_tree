
from datetime import date
from django import forms
from django.core.exceptions import ValidationError

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
            'parents',
            'spouse',
        )
        widgets = {
            'birthday': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }

    def clean(self):
        birthday_date = self.cleaned_data['birthday']
        death_date = self.cleaned_data['date_of_death']

        if isinstance(birthday_date, date) and isinstance(death_date, date) and death_date < birthday_date:
            raise ValidationError('Дата смерти не может быть раньше даты рождения!')