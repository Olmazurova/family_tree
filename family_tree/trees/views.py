from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView

from .models import Tree

NUMBER_OF_TREES = 10


class HomeView(ListView):
    """Представление главной страницы сайта."""

    model = Tree
    paginate_by = NUMBER_OF_TREES
    template_name = 'trees/home.html'
    queryset = Tree.objects.filter(is_public=True).order_by('created_at')


class MyTreeList(ListView):
    """Представление списка древ Рода, владельцем которых являтеся пользователь."""

    model = Tree
    paginate_by = NUMBER_OF_TREES
    template_name = 'trees/list.html'

    def get_queryset(self):
        return Tree.objects.filter(owner=self.request.user)


class TreeDetail(DetailView):
    """Представление подробной информации о древе Рода."""

    pass


class TreeCreate(CreateView):
    """Представления создания нового древа Рода."""

    pass


class TreeDelete(DeleteView):
    """Представление удаления древа Рода."""

    pass


class TreeUpdate(UpdateView):
    """Представление редактирования древа Рода."""

    pass


class PersonDetail(DetailView):
    """Представление подробной информации о члене древа Рода."""

    pass


class PersonCreate(CreateView):
    """Представление создания нового члена древа Рода."""

    pass


class PersonUpdate(UpdateView):
    """Представление редактирования члена древа Рода."""

    pass


class PersonDelete(DeleteView):
    """Представление удаления члена древа Рода."""

    pass





