from datetime import timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from trees.models import Tree, Person

IMAGE_FILE = 'test_image.jpg'

URL_HOME = reverse_lazy('home')
URL_LOGIN = reverse_lazy('login')
URL_REG = reverse_lazy('registration')
URL_RULES = reverse_lazy('rules')
URL_TREE_LIST = reverse_lazy('trees:tree_list')
URL_TREE_CREATE = reverse_lazy('trees:tree_create')
URL_USER_EDIT = reverse_lazy('users:profile_edit')
URL_USER_LOGOUT = reverse_lazy('users:profile_logout')


# фикстуры юзеров и клиентов

@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create(username='simple_user')


@pytest.fixture
def author_tree(django_user_model):
    return django_user_model.objects.create(username='author_pedigree')


@pytest.fixture
def another_user_client(another_user):
    client = Client()
    client.force_login(another_user)
    return client


@pytest.fixture
def author_tree_client(author_tree):
    client = Client()
    client.force_login(author_tree)
    return client


# фикстуры родословных и их членов

@pytest.fixture
def public_tree(author_tree):
    return Tree.objects.create(
        genus_name='Новая родословная',
        owner=author_tree,
        slug='new_rodoslovnaya',
        is_public=True,
    )


@pytest.fixture
def member_public_tree(public_tree):
    person = Person.objects.create(
        surname='Иванов',
        name='Михаил',
        gender='м',
        photo=IMAGE_FILE,
    )
    person.genus_name.add(public_tree)
    person.save()
    public_tree.progenitor = person
    public_tree.save()
    return person


@pytest.fixture
def linked_public_tree(author_tree, public_tree):
    tree = Tree.objects.create(
        genus_name='Связанная родословная',
        owner=author_tree,
        slug='linked_rodoslovnaya',
        is_public=True,
    )
    tree.linked_tree.add(public_tree)
    tree.save()
    return tree


@pytest.fixture
def non_public_tree(author_tree):
    return Tree.objects.create(
        genus_name='Закрытая родословная',
        owner=author_tree,
        slug='zakr_rodoslovnaya',
        is_public=False,
    )


@pytest.fixture
def member_non_public_tree(non_public_tree):
    person = Person.objects.create(
        surname='Сидорова',
        name='Людмила',
        gender='ж',
    )
    person.genus_name.add(non_public_tree)
    person.save()
    non_public_tree.progenitor = person
    non_public_tree.save()
    return person


@pytest.fixture
def lots_of_trees(author_tree):
    for i in range(settings.ITEMS_COUNT_OF_PAGE + 1):
        tree = Tree.objects.create(
            genus_name=f'Родословная № {i}',
            owner=author_tree,
            slug=f'rodoslovnaya_{i}',
            is_public=True,
        )
        tree.save()


@pytest.fixture
def lots_of_members(author_tree, public_tree):
    now = timezone.now()
    for i in range(settings.ITEMS_COUNT_OF_PAGE + 1):
        person = Person.objects.create(
            surname=f'Фамилия {i}',
            name=f'Имя {i}',
            gender='м' if i // 2 == 0 else 'ж',
            birthday=now - timedelta(days=i * 30)
        )
        person.genus_name.add(public_tree)
        person.save()


# Фикстуры для создания url

@pytest.fixture
def url_tree_detail(public_tree):
    return reverse('trees:tree_detail', args=(public_tree.slug,))


@pytest.fixture
def url_non_public_tree_detail(non_public_tree):
    return reverse('trees:tree_detail', args=(non_public_tree.slug,))


@pytest.fixture
def url_tree_edit(public_tree):
    return reverse('trees:tree_edit', args=(public_tree.slug,))


@pytest.fixture
def url_tree_delete(public_tree):
    return reverse('trees:tree_delete', args=(public_tree.slug,))


@pytest.fixture
def url_tree_structure(public_tree, member_public_tree):
    return reverse('trees:tree_structure', args=(public_tree.slug,))


@pytest.fixture
def url_non_public_tree_structure(non_public_tree, member_non_public_tree):
    return reverse('trees:tree_structure', args=(non_public_tree.slug,))


@pytest.fixture
def url_person_create(public_tree):
    return reverse('trees:person_create', args=(public_tree.slug,))


@pytest.fixture
def url_person_detail(public_tree, member_public_tree):
    return reverse('trees:person', args=(public_tree.slug, member_public_tree.id))


@pytest.fixture
def url_non_public_person_detail(non_public_tree, member_non_public_tree):
    return reverse('trees:person', args=(non_public_tree.slug, member_non_public_tree.id))


@pytest.fixture
def url_person_edit(public_tree, member_public_tree):
    return reverse('trees:person_edit', args=(public_tree.slug, member_public_tree.id))


@pytest.fixture
def url_person_delete(public_tree, member_public_tree):
    return reverse('trees:person_delete', args=(public_tree.slug, member_public_tree.id))


@pytest.fixture
def url_user_profile(another_user):
    return reverse('users:profile', args=(another_user.username,))
