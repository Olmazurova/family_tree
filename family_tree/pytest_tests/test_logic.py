import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazy_fixtures import lf

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

def check_iterable(iterable_1, iterable_2):
    if len(iterable_1) == len(iterable_2):
        result = [item_1 == item_2 for item_1, item_2 in zip(iterable_1, iterable_2)]
        return all(result)
    return False


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, form_data, entity',
    (
            (URL_TREE_CREATE, FORM_DATA_TREE, Tree),
            (lf('url_person_create'), FORM_DATA_MEMBER, Person),
    )
)
@pytest.mark.parametrize(
    'parametrize_client, redirect_url, result',
    (
            (lf('client'), URL_LOGIN, True),
            (lf('another_user_client'), lf('url_tree_detail'), True),
    ),
)
def test_different_users_can_or_cant_create(
        url,
        form_data,
        parametrize_client,
        entity,
        redirect_url,
        result,
        client
):
    """
    Проверка, что аноним и авторизованный пользователь может или не может:
    - создать древо;
    - добавить члена родословной.
    """
    entity.objects.all().delete()
    entity_list_before = entity.objects.all()
    if parametrize_client == client:
        expected_url = f'{redirect_url}?next={url}'
    else:
        expected_url = redirect_url
    response = parametrize_client.post(url, data=form_data)
    assertRedirects(response, expected_url)

    entity_list_after = entity.objects.all()
    assert check_iterable(entity_list_before, entity_list_after) is result

@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, parametrize_client, entity, form_data, redirect_url, result',
    (
            (lf('url_tree_edit'), lf('client'), Tree, FORM_DATA_EDIT_TREE, URL_LOGIN, True),
            (lf('url_person_edit'), lf('client'), Person, FORM_DATA_MEMBER_EDIT, URL_LOGIN, True),
            (lf('url_tree_edit'), lf('another_user_client'), Tree, FORM_DATA_EDIT_TREE, lf('url_tree_detail'), True),
            (lf('url_person_edit'), lf('another_user_client'), Person, FORM_DATA_MEMBER_EDIT, lf('url_tree_detail'), True),
    )
)
def test_anonymous_cant_do(url, entity, form_data, parametrize_client, redirect_url, result, client):
    """
    Проверка, что аноним и авторизованный пользователь не может:
    - редактировать древо;
    - редактировать члена родословной.
    """
    entity_list_before = entity.objects.all()
    if parametrize_client == client:
        expected_url = f'{redirect_url}?next={url}'
    else:
        expected_url = redirect_url
    response = parametrize_client.post(url, data=form_data)
    assertRedirects(response, expected_url)

    entity_list_after = entity.objects.all()
    assert check_iterable(entity_list_before, entity_list_after) is result
