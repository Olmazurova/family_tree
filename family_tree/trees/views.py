from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from pytils.translit import slugify

from .models import Tree, Person
from .forms import TreeForm, PersonForm

NUMBER_OF_TREES = 10


class HomeView(ListView):
    """Представление главной страницы сайта."""

    model = Tree
    paginate_by = NUMBER_OF_TREES
    template_name = 'trees/home.html'
    queryset = Tree.objects.filter(is_public=True)


class MyTreeList(LoginRequiredMixin, ListView):
    """Представление списка древ Рода, владельцем которых являтеся пользователь."""

    model = Tree
    paginate_by = NUMBER_OF_TREES
    template_name = 'trees/list.html'

    def get_queryset(self):
        return Tree.objects.filter(owner=self.request.user)


class TreeDetail(DetailView):
    """Представление подробной информации о древе Рода."""

    model = Tree
    template_name = 'trees/tree_detail.html'
    context_object_name = 'tree_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trees'] = Tree.objects.filter(linked_tree=context['tree_obj'].id)
        context['members'] = Person.objects.filter(genus_name=context['object'].id)
        print(context)
        for mem in context['members']:
            print(mem.genus_name)
        return context


class TreeCreate(LoginRequiredMixin, CreateView):
    """Представления создания нового древа Рода."""

    model = Tree
    form_class = TreeForm
    template_name = 'trees/create_tree.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.genus_name)
        return super().form_valid(form)


class TreeDelete(DeleteView):
    """Представление удаления древа Рода."""

    model = Tree
    template_name = 'trees/create_tree.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Tree, slug=self.kwargs['slug'])
        form = TreeForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context


class TreeUpdate(UpdateView):
    """Представление редактирования древа Рода."""

    model = Tree
    form_class = TreeForm
    template_name = 'trees/create_tree.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Tree, slug=self.kwargs['slug'])
        form = TreeForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context


class PersonDetail(LoginRequiredMixin, DetailView):
    """Представление подробной информации о члене древа Рода."""

    model = Person
    template_name = 'trees/person_detail.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Person, id=self.kwargs['id'])
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_tree'] = Tree.objects.get(person_id=self.kwargs['id'])
        context['children'] = Person.objects.filter(Q(father=self.kwargs['id']) | Q(mother=self.kwargs['id']))
        print(kwargs['object'])
        print(context)
        return context


class PersonCreate(LoginRequiredMixin, CreateView):
    """Представление создания нового члена древа Рода."""

    model = Person
    form_class = PersonForm
    template_name = 'trees/person_create.html'
    success_url = reverse_lazy('home')

    # def form_valid(self, form):
    #     new_person = form.instance
    #     new_person.save()
    #     new_person.genus_name = Tree.objects.get(slug=self.kwargs['slug']).id
    #     # tree_obj = Tree.objects.get(slug=self.kwargs['slug']).id
    #     # form.instance.genus_name.set(tree_obj)
    #     return super().form_valid(form)



class PersonUpdate(LoginRequiredMixin, UpdateView):
    """Представление редактирования члена древа Рода."""

    model = Person
    form_class = PersonForm
    template_name = 'trees/person_create.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return get_object_or_404(Person, id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        form = PersonForm(self.request.POST or None, instance=instance)
        context['form'] = form
        return context


class PersonDelete(LoginRequiredMixin, DeleteView):
    """Представление удаления члена древа Рода."""

    model = Person
    template_name = 'trees/person_create.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset =None):
        return get_object_or_404(Person, id=self.kwargs['id'])

    # Он здесь нужен???
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Person, pk=self.kwargs['id'])
        form = PersonForm(self.request.POST or None, instance=instance)
        context['form'] = form
        print(context)
        return context


class RulesView(TemplateView):
    """Представление страницы правил проекта 'древо Рода'"""

    template_name = 'rules.html'
