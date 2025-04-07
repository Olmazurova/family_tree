import pytest
from pytest_lazy_fixtures import lf
from django.conf import settings

from .conftest import URL_HOME, URL_TREE_LIST

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
def
# тесты медиа

# тесты вывода данных
def test():
    pass