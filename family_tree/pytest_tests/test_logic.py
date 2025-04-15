from typing import Sequence

import pytest
from django.test.client import Client
from pytest_django.asserts import assertRedirects, assertFormError
from pytest_lazy_fixtures import lf
from pytils.translit import slugify

from trees.models import Tree, Person
from .conftest import URL_TREE_CREATE, URL_LOGIN, URL_TREE_LIST

from family_tree.pytest_tests.conftest import public_tree

FORM_DATA_TREE = {
    'genus_name': 'Ещё одна родословная',
    'is_public': True,
}

FORM_DATA_MEMBER = {
    'genus_name': lf('public_tree'),
    'surname': 'Сидоров',
    'name': 'Олег',
    'gender': 'м',
}

FORM_DATA_EDIT_TREE = {
    'info': 'Новое описание родословной',
    'is_public': False,
}

FORM_DATA_MEMBER_EDIT = {
    'surname': 'Помидоров',
}

WARNING = 'Древо с таким Идентификатор уже существует.'


def check_iterable(sequence_1: Sequence, sequence_2: Sequence) -> bool:
    if len(sequence_1) == len(sequence_2):
        result = [item_1 == item_2
                  for item_1, item_2
                  in zip(sequence_1, sequence_2)]
        return all(result)
    return False


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, form_data, entity, redirect_url',
    (
        (URL_TREE_CREATE, FORM_DATA_TREE, Tree, URL_LOGIN),
        (lf('url_person_create'), FORM_DATA_MEMBER, Person, URL_LOGIN),
        (lf('url_tree_edit'), FORM_DATA_EDIT_TREE, Tree, lf('url_tree_detail')),
        (lf('url_person_edit'),
         FORM_DATA_MEMBER_EDIT,
         Person,
         lf('url_tree_detail')
         ),
    )
)
def test_anonymous_cant_do(
        url: str,
        form_data: dict,
        entity: Tree | Person,
        redirect_url: str,
        client: Client
) -> None:
    """
    Проверка, что аноним не может:
    - создать древо;
    - добавить члена родословной;
    - редактировать древо;
    - редактировать члена родословной.
    """
    entity_list_before = entity.objects.all()
    expected_url = f'{redirect_url}?next={url}'
    response = client.post(url, data=form_data)
    assertRedirects(response, expected_url)

    entity_list_after = entity.objects.all()
    assert check_iterable(entity_list_before, entity_list_after)


@pytest.mark.parametrize(
    'parametrize_client, url, form_data, entity, redirect_url, result',
    (
        (lf('another_user_client'),
         lf('url_person_create'),
         FORM_DATA_MEMBER,
         Person,
         lf('url_tree_detail'),
         True
         ),
        (lf('author_tree_client'),
         URL_TREE_CREATE,
         FORM_DATA_TREE,
         Tree,
         URL_TREE_LIST,
         False
         ),
        (lf('author_tree_client'),
         lf('url_person_create'),
         FORM_DATA_MEMBER,
         Person,
         lf('url_tree_detail'),
         False
         ),
    )
)
def test_different_users_can_or_cant_create(
        parametrize_client: Client,
        url: str,
        form_data: dict,
        entity: Tree | Person,
        redirect_url: str,
        result: bool
) -> None:
    """
     Проверка, что авторизованный пользователь и автор может или не может:
    - создать древо;
    - добавить члена родословной;
    """
    entity_list_before = entity.objects.all()
    print(entity_list_before)
    response = parametrize_client.post(url, data=form_data)
    assertRedirects(response, redirect_url)

    entity_list_after = entity.objects.all()
    print(entity_list_after)
    assert check_iterable(entity_list_before, entity_list_after) is result
    

@pytest.mark.parametrize(
    'parametrize_client, result',
    (
        (lf('another_user_client'), False),
        (lf('author_tree_client'), True),
    )
)
def test_different_users_can_or_cant_edit_tree(
        parametrize_client: Client,
        result: bool,
        url_tree_edit: str,
        url_tree_detail: str,
        public_tree: Tree,
) -> None:
    """
     Проверка, что авторизованный пользователь не может,
     а автор может редактировать древо.
    """
    tree = Tree.objects.get(id=public_tree.id)
    response = parametrize_client.post(url_tree_edit, data=FORM_DATA_EDIT_TREE)
    assertRedirects(response, url_tree_detail)

    tree.refresh_from_db()
    assert (tree.info == FORM_DATA_EDIT_TREE['info']) is result
    assert (tree.is_public == FORM_DATA_EDIT_TREE['is_public']) is result


@pytest.mark.parametrize(
    'parametrize_client, result',
    (
        (lf('another_user_client'), False),
        (lf('author_tree_client'), True),
    )
)
def test_different_users_can_or_cant_edit_member(
        parametrize_client: Client,
        result: bool,
        url_person_edit: str,
        url_tree_detail: str,
        member_public_tree: Person,
) -> None:
    """
     Проверка, что авторизованный пользователь не может,
     а автор может редактировать члена родословной.
    """
    member = member_public_tree
    response = parametrize_client.post(
        url_person_edit,
        data=FORM_DATA_MEMBER_EDIT
    )
    assertRedirects(response, url_tree_detail)

    member.refresh_from_db()
    assert (member.surname == FORM_DATA_MEMBER_EDIT['surname']) is result


@pytest.mark.parametrize(
    'parametrize_client, url, entity, redirect_url, result',
    (
            (lf('client'), lf('url_tree_delete'), Tree, URL_TREE_LIST, True),
            (lf('client'),
             lf('url_person_delete'),
             Person,
             lf('url_tree_detail'),
             True
             ),
            (lf('another_user_client'),
             lf('url_tree_delete'),
             Tree,
             URL_TREE_LIST,
             True
             ),
            (lf('another_user_client'),
             lf('url_person_delete'),
             Person,
             lf('url_tree_detail'),
             True
             ),
            (lf('author_tree_client'),
             lf('url_tree_delete'),
             Tree,
             URL_TREE_LIST,
             False
             ),
            (lf('author_tree_client'),
             lf('url_person_delete'),
             Person,
             lf('url_tree_detail'),
             False
             ),
    )
)
def test_different_users_can_or_cant_delete(
        parametrize_client: Client,
        url: str,
        entity: Tree | Person,
        redirect_url: str,
        result: bool,
) -> None:
    """
    Проверка, что аноним и авторизованный пользователь не могут,
    а автор может удалить древо и члена родословной.
    """
    entity_list_before = entity.objects.values().all()
    response = parametrize_client.delete(url)
    assertRedirects(response, redirect_url)

    entity_list_after = entity.objects.values().all()
    assert check_iterable(entity_list_before, entity_list_after) is result


def test_slug_formation_creation_tree(another_user_client: Client) -> None:
    """
    Проверка, что если слаг не задан, при создании древа -
    он формируется автоматически.
    """
    Tree.objects.all().delete()
    response = another_user_client.post(URL_TREE_CREATE, data=FORM_DATA_TREE)
    assertRedirects(response, URL_TREE_LIST)
    tree = Tree.objects.last()
    assert tree.slug == slugify(FORM_DATA_TREE['genus_name'])


def test_cant_creation_tree_with_repeating_slug(
        another_user_client: Client,
        public_tree: Tree
) -> None:
    """Проверка, что нельзя создать древо с повторяющимся слагом."""
    trees_before = Tree.objects.all()
    form_with_repeat_slug = FORM_DATA_TREE.update(slug=public_tree.slug)
    response = another_user_client.post(
        URL_TREE_CREATE,
        data=form_with_repeat_slug
    )
    assertFormError(response.context['form'], field='slug', errors=[])

    trees_after = Tree.objects.all()
    assert check_iterable(trees_before, trees_after)
