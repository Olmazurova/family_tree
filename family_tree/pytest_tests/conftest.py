import pytest
from django.test.client import Client
from django.urls import reverse

from trees.models import Tree, Person


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


@pytest.fixture
def public_tree(author_tree):
    return Tree.objects.create(
        genus_name='Новая родословная',
        owner=author_tree,
        slug='new_rodoslovnaya',
        is_public=True,
    )


@pytest.fixture
def member_tree(public_tree):
    person = Person.objects.create(
        # genus_name=public_tree,
        surname='Иванов',
        name='Михаил',
        gender='м',
    )
    person.genus_name.add(public_tree)
    return person


@pytest.fixture
def url_tree_detail(public_tree):
    return reverse('trees:tree_detail', args=(public_tree.slug,))


@pytest.fixture
def url_tree_edit(public_tree):
    return reverse('trees:tree_edit', args=(public_tree.slug,))


@pytest.fixture
def url_tree_delete(public_tree):
    return reverse('trees:tree_delete', args=(public_tree.slug,))


@pytest.fixture
def url_tree_structure(public_tree):
    return reverse('trees:tree_structure', args=(public_tree.slug,))


@pytest.fixture
def url_person_create(public_tree):
    return reverse('trees:person_create', args=(public_tree.slug,))


@pytest.fixture
def url_person_detail(public_tree, member_tree):
    return reverse('trees:person', args=(public_tree.slug, member_tree.id))


@pytest.fixture
def url_person_edit(public_tree, member_tree):
    return reverse('trees:person_edit', args=(public_tree.slug, member_tree.id))


@pytest.fixture
def url_person_delete(public_tree, member_tree):
    return reverse('trees:person_delete', args=(public_tree.slug, member_tree.id))


@pytest.fixture
def url_user_profile(another_user):
    return reverse('users:profile', args=(another_user.username,))
