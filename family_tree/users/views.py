from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import UserForm, UserEditForm

User = get_user_model()


class UserCreate(CreateView):
    """Представление создания нового пользователя."""

    template_name = 'registration/registration_form.html'
    form_class = UserForm
    success_url = 'home'


class UserProfileDetail(DetailView):
    """Представление информации профиля пользователя."""

    model = User
    template_name = 'users/profile.html'


class UserProfileUpdate(UpdateView):
    """Представление редактирования профиля пользователя."""

    model = User
    form_class = UserEditForm
    template_name = 'users/profile_edit.html'





