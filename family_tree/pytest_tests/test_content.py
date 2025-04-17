import pytest
from pytest_lazy_fixtures import lf
from django.conf import settings

from .conftest import URL_HOME, URL_TREE_LIST, URL_TREE_CREATE
from trees.forms import TreeForm, PersonForm

IMAGE_FILE = 'test_image.jpg'


# тесты пагинации

@pytest.mark.usefixtures('lots_of_trees', 'lots_of_members')
@pytest.mark.parametrize(
    'url, key',
    (
            (URL_HOME, 'object_list'),
            (URL_TREE_LIST, 'object_list'),
            (lf('url_tree_detail'), 'page_obj'),
    )
)
def test_page_pagination(url, key, author_tree_client):
    """Проверяет количество выводимых объектов на страницах."""
    response = author_tree_client.get(url)
    items_count = len(response.context[key])
    assert items_count == settings.ITEMS_COUNT_OF_PAGE


# тесты сортировки

@pytest.mark.usefixtures('lots_of_trees')
@pytest.mark.parametrize(
    'url',
    (
            URL_HOME,
            URL_TREE_LIST,
    )
)
def test_order_trees_on_page(url, author_tree_client):
    """Проверка порядка вывода родословных на странице."""
    response = author_tree_client.get(url)
    response_items_list = [tree.created_at
                           for tree
                           in response.context['object_list']
                           ]
    expected_items_list = sorted(response_items_list)
    assert response_items_list == expected_items_list


@pytest.mark.usefixtures('lots_of_members')
def test_order_members_on_page(url_tree_detail, author_tree_client):
    """Проверка порядка вывода членов родословной на странице."""
    response = author_tree_client.get(url_tree_detail)
    response_items_list = [member.birthday
                           for member
                           in response.context['page_obj']
                           ]
    expected_items_list = sorted(response_items_list)
    assert response_items_list == expected_items_list


# тесты медиа
@pytest.mark.usefixtures('public_tree', 'author_tree', 'member_public_tree')
@pytest.mark.parametrize(
    'url',
    (lf('url_person_detail'), lf('url_person_delete'))
)
def test_has_image_on_pages_person(url, author_tree_client):
    """Проверка вывода фото члена родословной на страницы."""
    expected_url = f'{settings.MEDIA_URL}{IMAGE_FILE}'
    print(expected_url)
    response = author_tree_client.get(url)
    image_url = response.context['person'].photo.url
    print(response.context['object'].photo)
    assert image_url == expected_url


# тесты вывода данных
@pytest.mark.parametrize(
    'url, tree_or_member, key_list, show_tree',
    (
            (URL_HOME, lf('public_tree'), 'object_list', True),
            (URL_HOME, lf('non_public_tree'), 'object_list', False),
            (lf('url_tree_detail'), lf('linked_public_tree'), 'trees', True),
            (lf('url_tree_detail'), lf('member_public_tree'), 'page_obj', True),
            (URL_TREE_LIST, lf('public_tree'), 'object_list', True),
            (URL_TREE_LIST, lf('non_public_tree'), 'object_list', True),
    )
)
def test_tree_or_member_in_list_page(
        url,
        tree_or_member,
        key_list,
        show_tree,
        author_tree_client,
        public_tree
):
    """Проверка наличия (отсутствия) древа или члена рода в списке на странице."""
    response = author_tree_client.get(url)
    object_list = response.context[key_list]
    assert (tree_or_member in object_list) is show_tree


def test_unavailable_other_trees_in_my_list(
        another_user_client,
        public_tree,
        non_public_tree
):
    """Проверка недоступности чужих родословных в списке родословных пользователя."""
    response = another_user_client.get(URL_TREE_LIST)
    object_list = response.context.get('object_list')
    assert public_tree not in object_list
    assert non_public_tree not in object_list


@pytest.mark.parametrize(
    'url, expected_info, key_context',
    (
            (lf('url_tree_detail'), lf('public_tree'), 'tree_obj'),
            (lf('url_person_detail'), lf('member_public_tree'), 'person'),
            (lf('url_tree_structure'), lf('member_public_tree'), 'ancestor'),
            (lf('url_person_delete'), lf('member_public_tree'), 'person'),
            (lf('url_tree_delete'), lf('public_tree'), 'tree')
    )
)
def test_correct_output_information_on_pages(
        url,
        expected_info,
        key_context,
        author_tree_client
):
    """Проверка, что на страницу передаётся ожидаемая информация."""
    response = author_tree_client.get(url)
    received_information = response.context.get(key_context)
    assert received_information == expected_info


# тесты формы

@pytest.mark.parametrize(
    'url, form_type',
    (
            (URL_TREE_CREATE, TreeForm),
            (lf('url_tree_edit'), TreeForm),
            (lf('url_person_create'), PersonForm),
            (lf('url_person_edit'), PersonForm),
    )
)
def test_displaying_form_on_pages(url, form_type, author_tree_client):
    """Проверяет наличие формы на страницах."""
    response = author_tree_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], form_type)


@pytest.mark.parametrize(
    'url, expected_form',
    (
            (lf('url_tree_delete'), TreeForm),
            (lf('url_person_delete'), PersonForm),
    )
)
def test_absence_form_on_pages(url, expected_form, author_tree_client):
    """Проверяет отсутствие отображения формы на страницах."""
    response = author_tree_client.get(url)
    form = response.context.get('form')
    # проверка идёт по сущности формы, т.к. даже при удалении в контексте есть ключ 'form'
    assert not isinstance(form, expected_form)
