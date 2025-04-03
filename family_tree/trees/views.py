from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Min
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


class TreeDetail(LoginRequiredMixin, DetailView):
    """Представление подробной информации о древе Рода."""

    model = Tree
    template_name = 'trees/tree_detail.html'
    context_object_name = 'tree_obj'

    def get_object(self, queryset=None):
        obj = Tree.objects.get(slug=self.kwargs['slug'])
        if obj.owner == self.request.user.id:
            return obj
        else:
            return get_object_or_404(Tree, slug=self.kwargs['slug'], is_public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # kl = Tree.objects.filter(pogenitor__isnull=False)
        ancestor = context['tree_obj'].progenitor
        context['trees'] = Tree.objects.filter(linked_tree=context['tree_obj'].id)
        context['members'] = Person.objects.filter(genus_name=context['tree_obj'].id)
        context['ancestor'] = ancestor
        return context


class TreeStructure(LoginRequiredMixin, DetailView):
    model = Tree
    template_name = 'trees/tree_structure.html'
    context_object_name = 'tree_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ancestor = Person.objects.filter(id=context['tree_obj'].progenitor.id).select_related('spouse')
        context['ancestor'] = ancestor[0]
        print(ancestor)
        print(ancestor[0])
        print(ancestor[0].child.all().count())
        print(ancestor[0].my_child)
        print(ancestor[0].my_child.all)
        return context


class TreeImage(LoginRequiredMixin, DetailView):
    model = Tree
    template_name = 'trees/tree_image.html'
    context_object_name = 'tree_obj'



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


class TreeDelete(UserPassesTestMixin, DeleteView):
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

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user.id


class TreeUpdate(UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


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
        return context


class PersonCreate(UserPassesTestMixin, CreateView):
    """Представление создания нового члена древа Рода."""

    model = Person
    form_class = PersonForm
    template_name = 'trees/person_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        new_person = form.instance
        new_person.save()
        if new_person.father:
            father = new_person.father
            father.child.add(new_person)
            father.save()
        if new_person.mother:
            mother = new_person.mother
            mother.child.add(new_person)
            mother.save()
        if new_person.spouse:
            spouse = new_person.spouse
            spouse.spouse = new_person
            spouse.save()

        # new_person.genus_name = Tree.objects.get(slug=self.kwargs['slug']).id
        # tree_obj = Tree.objects.get(slug=self.kwargs['slug']).id
        # form.instance.genus_name.set(tree_obj)
        return super().form_valid(form)

    def test_func(self):
        tree = Tree.objects.get(slug=self.kwargs['slug'])
        return tree.owner == self.request.user


class PersonUpdate(UserPassesTestMixin, UpdateView):
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

    def test_func(self):
        person = self.get_object()
        tree = Tree.objects.get(slug=self.kwargs['slug'])
        return tree.owner == self.request.user and person in tree.person_id.all()

    def form_valid(self, form):
        new_person = form.instance
        new_person.save()
        if new_person.father:
            father = new_person.father
            father.my_child.add(new_person)
            father.save()
        if new_person.mother:
            mother = new_person.mother
            mother.my_child.add(new_person)
            mother.save()
        if new_person.spouse:
            spouse = new_person.spouse
            spouse.my_spouse.add(new_person)
            spouse.save()

        # new_person.genus_name = Tree.objects.get(slug=self.kwargs['slug']).id
        # tree_obj = Tree.objects.get(slug=self.kwargs['slug']).id
        # form.instance.genus_name.set(tree_obj)
        return super().form_valid(form)


class PersonDelete(UserPassesTestMixin, DeleteView):
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
        return context

    def test_func(self):
        person = self.get_object()
        tree = Tree.objects.get(owner=self.request.user.id)
        return person.genus_name == tree.id
