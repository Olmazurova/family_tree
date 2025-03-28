from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserForm(UserCreationForm):
    """Форма создания нового пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'about_oneself',
            'photo',
            'birthday',
        )

class UserEditForm(UserChangeForm):
    """Форма редактирования пользователя."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'about_oneself',
            'photo',
            'birthday',
        )