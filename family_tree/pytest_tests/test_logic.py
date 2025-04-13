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
        result = [item_1 == item_2
                  for item_1, item_2
                  in zip(iterable_1, iterable_2)]
        return all(result)
    return False


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, form_data, entity, redirect_url',
    (
        (URL_TREE_CREATE, FORM_DATA_TREE, Tree, URL_LOGIN),
        (lf('url_person_create'), FORM_DATA_MEMBER, Person, URL_LOGIN),
        (lf('url_tree_edit'), FORM_DATA_EDIT_TREE, Tree, lf('url_tree_detail')),
        (lf('url_person_edit'), FORM_DATA_MEMBER_EDIT, Person, lf('url_tree_detail')),
    )
)
def test_anonymous_cant_do(url, form_data, entity, redirect_url, client):
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
        (lf('another_user_client'), lf('url_person_create'), FORM_DATA_MEMBER, Person, lf('url_tree_detail'), True),
        (lf('author_tree_client'), URL_TREE_CREATE, FORM_DATA_TREE, Tree, URL_TREE_LIST, False),
        (lf('author_tree_client'), lf('url_person_create'), FORM_DATA_MEMBER, Person, lf('url_tree_detail'), False),
    )
)
def test_different_users_can_or_cant_create(
        parametrize_client,
        url,
        form_data,
        entity,
        redirect_url,
        result
):
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
        parametrize_client,
        result,
        url_tree_edit,
        url_tree_detail,
        public_tree
):
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
        parametrize_client,
        result,
        url_person_edit,
        url_tree_detail,
        member_public_tree
):
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



    