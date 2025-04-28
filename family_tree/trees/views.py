from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from pytils.translit import slugify

from .forms import PersonForm, TreeForm
from .mixins import (ObjectPermissionMixin, PersonBaseViewMixin,
                     PersonViewAddFormKwargsMixin, TreeBaseViewMixin,
                     TreeCreateUpdateMixin, TreeListViewMixin, TreeObjectMixin)
from .models import Person, Tree
from .utils import form_valid_base, get_tree


class HomeView(TreeListViewMixin, ListView):
    """Представление главной страницы сайта."""

    template_name = 'trees/home.html'
    queryset = Tree.objects.filter(is_public=True)


class MyTreeList(LoginRequiredMixin, TreeListViewMixin, ListView):
    """Представление списка древ Рода, владельцем которых является пользователь."""

    template_name = 'trees/list.html'

    def get_queryset(self):
        return Tree.objects.filter(owner=self.request.user)


class TreeDetail(LoginRequiredMixin, TreeObjectMixin, DetailView):
    """Представление подробной информации о древе Рода."""

    template_name = 'trees/tree_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ancestor = context['tree_obj'].progenitor
        context['trees'] = Tree.objects.filter(
            linked_tree=context['tree_obj'].id
        )

        members = Person.objects.filter(
            genus_name=context['tree_obj'].id
        ).order_by('birthday')
        paginator = Paginator(members, settings.ITEMS_COUNT_OF_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['ancestor'] = ancestor
        return context


class TreeStructure(LoginRequiredMixin, TreeObjectMixin, DetailView):
    """Представление для показа родословной в виде иерархической структуры."""

    template_name = 'trees/tree_structure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ancestor = Person.objects.filter(
            id=context['tree_obj'].progenitor.id
        ).select_related('spouse')
        context['ancestor'] = ancestor[0]
        return context


class TreeCreate(LoginRequiredMixin, TreeCreateUpdateMixin, CreateView):
    """Представления создания нового древа Рода."""

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.genus_name)
        return super().form_valid(form)


class TreeDelete(ObjectPermissionMixin, TreeBaseViewMixin, DeleteView):
    """Представление удаления древа Рода."""

    template_name = 'trees/tree_create.html'


class TreeUpdate(ObjectPermissionMixin, TreeCreateUpdateMixin, UpdateView):
    """Представление редактирования древа Рода."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_tree(self)
        form = TreeForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    def get_success_url(self):
        return reverse(
            'trees:tree_detail',
            kwargs={'slug': self.kwargs['slug']},
        )


class PersonDetail(LoginRequiredMixin, PersonBaseViewMixin, DetailView):
    """Представление подробной информации о члене древа Рода."""

    template_name = 'trees/person_detail.html'

    def get_object(self, queryset=None):
        obj = get_tree(self)
        if obj.owner == self.request.user:
            return get_object_or_404(Person, id=self.kwargs['id'])

        else:
            return get_object_or_404(
                Person, id=self.kwargs['id'], genus_name__is_public=True
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_tree'] = Tree.objects.get(person_id=self.kwargs['id'])
        context['children'] = self.get_object().children.all()
        return context


class PersonCreate(
    ObjectPermissionMixin,
    PersonViewAddFormKwargsMixin,
    CreateView
):
    """Представление создания нового члена древа Рода."""

    form_class = PersonForm
    context_object_name = 'person'

    def form_valid(self, form):
        new_person = form_valid_base(form)
        tree = get_tree(self)
        members = Person.objects.filter(genus_name=tree)

        if not members:
            tree.progenitor = new_person
            tree.save()

        return super().form_valid(form)


class PersonUpdate(
    ObjectPermissionMixin,
    PersonViewAddFormKwargsMixin,
    UpdateView
):
    """Представление редактирования члена древа Рода."""

    form_class = PersonForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        form = PersonForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    def test_func(self):
        person = self.get_object()
        tree = get_tree(self)
        return (tree.owner == self.request.user
                and person in tree.person_id.all())

    def form_valid(self, form):
        form_valid_base(form)
        return super().form_valid(form)


class PersonDelete(ObjectPermissionMixin, PersonBaseViewMixin, DeleteView):
    """Представление удаления члена древа Рода."""

    pass
