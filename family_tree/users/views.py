from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy

from .forms import UserForm, UserEditForm

User = get_user_model()


class UserCreate(CreateView):
    """Представление создания нового пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserForm
    success_url = reverse_lazy('home')


class UserProfileDetail(DetailView):
    """Представление информации профиля пользователя."""

    model = User
    template_name = 'users/profile.html'
    slug_url_kwarg = 'username'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserProfileUpdate(UpdateView):
    """Представление редактирования профиля пользователя."""

    model = User
    form_class = UserEditForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('home')


class UserProfileLogout(TemplateView):
    """Представление выхода из профиля пользователя."""

    model = User
    template_name = 'users/profile_logout.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

