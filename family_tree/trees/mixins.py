from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .forms import TreeForm
from .models import Person, Tree
from .utils import get_tree


class TreeBaseViewMixin:
    """Базовый миксин представления родословной. Определяет модель."""

    model = Tree

    def get_success_url(self):
        return reverse('trees:tree_list')


class TreeListViewMixin(TreeBaseViewMixin):
    """Миксин добавляет параметр пагинации."""

    paginate_by = settings.ITEMS_COUNT_OF_PAGE


class TreeObjectMixin(TreeBaseViewMixin):
    """Добавляет context_object_name и переопределяет get_object."""

    context_object_name = 'tree_obj'

    def get_object(self, queryset=None):
        obj = get_tree(self)
        if obj.owner == self.request.user:
            return obj
        else:
            return get_object_or_404(
                Tree,
                slug=self.kwargs['slug'],
                is_public=True
            )


class TreeCreateUpdateMixin(TreeBaseViewMixin):
    """Миксин добавляет форму и шаблон."""

    form_class = TreeForm
    template_name = 'trees/tree_create.html'


class ObjectPermissionMixin(UserPassesTestMixin):
    """Миксин добавляет методы test_func и handle_no_permission."""

    def test_func(self):
        obj = get_tree(self)
        return obj.owner == self.request.user

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class PersonBaseViewMixin:
    """Базовый миксин представления члена родословной."""

    model = Person
    template_name = 'trees/person_create.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Person, id=self.kwargs['id'])

    def get_success_url(self):
        return reverse(
            'trees:tree_detail',
            kwargs={'slug': self.kwargs['slug']}
        )


class PersonViewAddFormKwargsMixin(PersonBaseViewMixin):
    """Миксин представления члена родословной, переопределяет get_form_kwargs."""

    def get_form_kwargs(self, *args, **kwargs):
        tree = get_tree(self)
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs.update(tree=tree)
        return kwargs
