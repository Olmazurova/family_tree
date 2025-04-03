from django.contrib.auth import get_user_model
from django.db import models

from .utils import change_owner_or_delete, get_progenitor

LENGTH_SURNAME = 100
LENGTH_NAME = 50
GENDER_CHOICE = (('м', 'Мужской'), ('ж', 'Женский'))

User = get_user_model()


class Tree(models.Model):
    """Описывает древо рода."""

    genus_name = models.CharField(
        'Имя рода',
        max_length=LENGTH_SURNAME,
    )
    created_at = models.DateTimeField(
        'Создано',
        auto_now_add=True,
    )
    changed_at = models.DateTimeField(
        'Изменено',
        blank=True,
        auto_now=True,
    )
    info = models.TextField(
        'Описание',
        blank=True,
    )
    linked_tree = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='Связанное древо'
    )
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.SET(change_owner_or_delete),
        related_name='tree_owner',
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичное',
        help_text='Поставьте галочку, чтобы сделать древо публичным.',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.'),
        blank=True,
    )
    progenitor = models.OneToOneField(
        'Person',
        verbose_name='Родоначальник',
        on_delete=models.SET_NULL,
        null=True,
        related_name='tree_progenitor',
        blank=True,
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Древо'
        verbose_name_plural = 'Древа'

    def __str__(self):
        return self.genus_name


class Person(models.Model):
    """Описывает конкретного человека."""

    genus_name = models.ManyToManyField(Tree, verbose_name='Род', related_name='person_id')
    surname = models.CharField('Фамилия', max_length=LENGTH_SURNAME)
    name = models.CharField(
        'Имя',
        max_length=LENGTH_NAME,
        blank=True,
    )
    maiden_name = models.CharField(
        'Девичья фамилия',
        max_length=LENGTH_SURNAME,
        blank=True,
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=LENGTH_NAME,
        blank=True,
    )
    birthday = models.DateField(
        'День рождения',
        blank=True,
        null=True,
    )
    date_of_death = models.DateField(
        'Дата смерти',
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICE,
        verbose_name='Пол',
    )
    biography = models.TextField(
        'Биография',
        blank=True,
    )
    photo = models.ImageField(
        'Фото',
        blank=True,
        upload_to='person_photo',
    )
    father = models.ForeignKey(
        'self',
        blank=True,
        verbose_name='Отец',
        on_delete=models.SET_NULL,
        null=True,
        related_name='my_father',
    )
    mother = models.ForeignKey(
        'Person',
        blank=True,
        verbose_name='Мать',
        on_delete=models.SET_NULL,
        null=True,
        related_name='my_mother',
    )
    spouse = models.ForeignKey(
        'Person',
        blank=True,
        verbose_name='Супруг',
        on_delete=models.SET_NULL,
        null=True,
        related_name='my_spouse',
    )
    child = models.ManyToManyField(
        'Person',
        blank=True,
        verbose_name='Ребёнок',
        # on_delete=models.SET_DEFAULT,
        # default='нет информации',
        related_name='my_child',
    )

    class Meta:
        verbose_name = 'член родословной'
        verbose_name_plural = 'Члены родословной'
        ordering = ('birthday',)

    def __str__(self):
        return f'{self.surname} {self.name}'

