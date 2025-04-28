from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import date


class FamilyTreeUser(AbstractUser):
    """
    Расширенная модель пользователя, включает дополнительные поля:
    - о себе,
    - день рождения,
    - фотография.
    """

    about_oneself = models.TextField("О себе", blank=True)
    birthday = models.DateField(
        "День рождения",
        blank=True,
        default=date(1, 1, 1),
    )
    photo = models.ImageField(
        "Фото",
        blank=True,
        upload_to="users_photo"
    )
