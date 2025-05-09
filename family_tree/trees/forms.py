from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Person, Tree
from .utils import WIDGET_SETTINGS



class TreeForm(forms.ModelForm):
    """Форма древа на основе модели древа."""

    class Meta:
        model = Tree
        exclude = (
            'created_at',
            'changed_at',
            'owner',
        )

    def __init__(self, *args, **kwargs):
        super(TreeForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            # фильтруем объекты, которые будут выводиться для выбора в форме
            self.fields['linked_tree'].queryset = Tree.objects.filter(
                Q(owner=self.instance.owner) or Q(is_public=True)
            )
            self.fields['progenitor'].queryset = Person.objects.filter(
                genus_name=self.instance
            )
        else:
            self.fields['linked_tree'].queryset = Tree.objects.filter(
                is_public=True
            )
            self.fields['progenitor'].queryset = Person.objects.none()


class PersonForm(forms.ModelForm):
    """Форма описания члена родословной на основе соответствующей модели."""

    class Meta:
        model = Person
        fields = (
            'genus_name',
            'surname',
            'name',
            'patronymic',
            'maiden_name',
            'birthday',
            'date_of_death',
            'gender',
            'biography',
            'photo',
            'parents',
            'spouse',
        )
        widgets = {
            'birthday': WIDGET_SETTINGS,
            'date_of_death': WIDGET_SETTINGS,
        }

    def __init__(self, *args, **kwargs):
        tree = kwargs.pop('tree', None)
        super(self.__class__, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            # фильтруем объекты, которые будут выводиться для выбора в форме
            trees = Tree.objects.filter(person_id=self.instance.id)
            self.fields['parents'].queryset = Person.objects.filter(
                genus_name__in=trees
            )
            self.fields['spouse'].queryset = Person.objects.filter(
                genus_name__in=trees
            ).filter(~Q(gender=self.instance.gender))

            self.fields['genus_name'].queryset = Tree.objects.filter(
                owner__in=[tree.owner for tree in trees]
            )
        else:
            self.fields['parents'].queryset = Person.objects.filter(
                genus_name=tree
            )
            self.fields['spouse'].queryset = Person.objects.filter(
                genus_name=tree
            ).filter(~Q(gender=self.instance.gender))

            self.fields['genus_name'].queryset = Tree.objects.filter(
                owner=tree.owner
            )


    def clean(self):
        birthday_date = self.cleaned_data['birthday']
        death_date = self.cleaned_data['date_of_death']

        if (
                isinstance(birthday_date, date)
                and isinstance(death_date, date)
                and death_date < birthday_date
        ):
            raise ValidationError(
                'Дата смерти не может быть раньше даты рождения!'
            )
