from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse, reverse_lazy
from pytils.translit import slugify

from .models import Tree, Person
from .forms import TreeForm, PersonForm
from .utils import form_valid_base


class HomeView(ListView):
    """Представление главной страницы сайта."""

    model = Tree
    paginate_by = settings.ITEMS_COUNT_OF_PAGE
    template_name = 'trees/home.html'
    queryset = Tree.objects.filter(is_public=True)


class MyTreeList(LoginRequiredMixin, ListView):
    """Представление списка древ Рода, владельцем которых является пользователь."""

    model = Tree
    paginate_by = settings.ITEMS_COUNT_OF_PAGE
    template_name = 'trees/list.html'

    def get_queryset(self):
        return Tree.objects.filter(owner=self.request.user)


class TreeDetail(LoginRequiredMixin, DetailView):
    """Представление подробной информации о древе Рода."""

    model = Tree
    template_name = 'trees/tree_detail.html'
    context_object_name = 'tree_obj'

    def get_object(self, queryset=None):
        obj = Tree.objects.get(slug=self.kwargs['slug'])
        if obj.owner == self.request.user:
            return obj
        else:
            return get_object_or_404(Tree, slug=self.kwargs['slug'], is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ancestor = context['tree_obj'].progenitor
        context['trees'] = Tree.objects.filter(linked_tree=context['tree_obj'].id)

        members = Person.objects.filter(
            genus_name=context['tree_obj'].id
        ).order_by('birthday')
        paginator = Paginator(members, settings.ITEMS_COUNT_OF_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['ancestor'] = ancestor
        return context


class TreeStructure(LoginRequiredMixin, DetailView):
    model = Tree
    template_name = 'trees/tree_structure.html'
    context_object_name = 'tree_obj'

    def get_object(self, queryset=None):
        obj = Tree.objects.get(slug=self.kwargs['slug'])
        if obj.owner == self.request.user:
            return obj
        else:
            return get_object_or_404(Tree, slug=self.kwargs['slug'], is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ancestor = Person.objects.filter(
            id=context['tree_obj'].progenitor.id
        ).select_related('spouse')
        context['ancestor'] = ancestor[0]
        return context


class TreeImage(LoginRequiredMixin, DetailView):
    model = Tree
    template_name = 'trees/tree_image.html'
    context_object_name = 'tree_obj'



class TreeCreate(LoginRequiredMixin, CreateView):
    """Представления создания нового древа Рода."""

    model = Tree
    form_class = TreeForm
    template_name = 'trees/tree_create.html'
    success_url = reverse_lazy('trees:tree_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.genus_name)
        return super().form_valid(form)


class TreeDelete(UserPassesTestMixin, DeleteView):
    """Представление удаления древа Рода."""

    model = Tree
    template_name = 'trees/tree_create.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Tree, slug=self.kwargs['slug'])

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def get_success_url(self):
        return reverse('trees:tree_list')

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class TreeUpdate(UserPassesTestMixin, UpdateView):
    """Представление редактирования древа Рода."""

    model = Tree
    form_class = TreeForm
    template_name = 'trees/tree_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Tree, slug=self.kwargs['slug'])
        form = TreeForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context

    # def post(self, request, *args, **kwargs):
    #     form = TreeForm(self.request.POST, self.request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(self.get_success_url())
    #     return render(request, self.template_name, {'form': form})

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def get_success_url(self):
        return reverse(
            'trees:tree_detail',
            kwargs={'slug': self.kwargs['slug']},
        )

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class PersonBaseViewMixin:
    """Базовый класс представления члена родословной."""

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
    """Класс представления члена родословной, переопределяет get_form_kwargs."""

    def get_form_kwargs(self, *args, **kwargs):
        tree = Tree.objects.get(slug=self.kwargs.get('slug'))
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs.update(tree=tree)
        return kwargs


class PersonPermissionMixin(UserPassesTestMixin):
    """
    Миксин представления члена рода,
    содержит функции определения разрешения и перенаправления.
    """

    def test_func(self):
        tree = Tree.objects.get(slug=self.kwargs['slug'])
        return tree.owner == self.request.user

    def handle_no_permission(self):
        return redirect(self.get_success_url())


class PersonDetail(LoginRequiredMixin, PersonBaseViewMixin, DetailView):
    """Представление подробной информации о члене древа Рода."""

    template_name = 'trees/person_detail.html'

    def get_object(self, queryset=None):
        obj = Tree.objects.get(slug=self.kwargs['slug'])
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


class PersonCreate(PersonPermissionMixin, PersonViewAddFormKwargsMixin, CreateView):
    """Представление создания нового члена древа Рода."""

    form_class = PersonForm
    context_object_name = 'person'

    def form_valid(self, form):
        new_person = form_valid_base(form)

        tree = Tree.objects.get(slug=self.kwargs['slug'])

        members = Person.objects.filter(genus_name=tree)
        if not members:
            tree.progenitor = new_person
            tree.save()

        return super().form_valid(form)


class PersonUpdate(PersonPermissionMixin, PersonViewAddFormKwargsMixin, UpdateView):
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
        tree = Tree.objects.get(slug=self.kwargs['slug'])
        return tree.owner == self.request.user and person in tree.person_id.all()

    def form_valid(self, form):
        form_valid_base(form)
        return super().form_valid(form)


class PersonDelete(PersonPermissionMixin, PersonBaseViewMixin, DeleteView):
    """Представление удаления члена древа Рода."""

    pass
