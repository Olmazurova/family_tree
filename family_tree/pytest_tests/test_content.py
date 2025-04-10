import pytest
from pytest_lazy_fixtures import lf
from django.conf import settings

from .conftest import URL_HOME, URL_TREE_LIST, another_user_client, url_person_detail

IMAGE_FILE = 'test_image.jpg'


# тесты формы

# тесты пагинации

@pytest.mark.usefixtures('lots_of_trees', 'lots_of_members')
@pytest.mark.parametrize(
    'url, key',
    (
            (URL_HOME, 'object_list'),
            (URL_TREE_LIST, 'object_list'),
            (lf('url_tree_detail'), 'members'),
    )
)
def test_page_pagination(url, key, author_tree_client):
    """Проверяет количество выводимых объектов на страницах."""
    response = author_tree_client.get(url)
    items_count = response.context[key].count()
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
    response_items_list = [tree.created_at for tree in response.context['object_list']]
    expected_items_list = sorted(response_items_list)
    assert response_items_list == expected_items_list


@pytest.mark.usefixtures('lots_of_members')
def test_order_members_on_page(url_tree_detail, author_tree_client):
    """Проверка порядка вывода членов родословной на странице."""
    response = author_tree_client.get(url_tree_detail)
    response_items_list = [member.birthday for member in response.context['members']]
    expected_items_list = sorted(response_items_list)
    assert response_items_list == expected_items_list

# тесты медиа
@pytest.mark.parametrize(
    'url',
    (lf('url_person_detail'), lf('url_person_delete'))
)
def test_has_image_on_pages_person(url, another_user_client):
    """Проверка вывода фото члена родословной на страницы."""
    expected_url = f'{settings.MEDIA_URL}{IMAGE_FILE}'
    response = another_user_client.get(url)
    image = response.context.get('person').photo
    assert image.url == expected_url
    with open(expected_url) as expected_image:
        assert image == expected_image



# тесты вывода данных