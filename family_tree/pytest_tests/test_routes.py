from http import HTTPStatus

import pytest
from django.urls import reverse, reverse_lazy
from pytest_lazy_fixtures import lf

from family_tree.pytest_tests.conftest import public_tree, member_tree, another_user

URL_HOME = reverse_lazy('home')
URL_LOGIN = reverse_lazy('login')
URL_REG = reverse_lazy('registration')
URL_RULES = reverse_lazy('rules')
URL_TREE_LIST = reverse_lazy('trees:tree_list')
URL_TREE_CREATE = reverse_lazy('trees:tree_create')
URL_USER_EDIT = reverse_lazy('users:profile_edit')
URL_USER_LOGOUT = reverse_lazy('users:profile_logout')



@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, expected_status',
    (
            (URL_HOME, HTTPStatus.OK),
            (URL_REG, HTTPStatus.OK),
            (URL_LOGIN, HTTPStatus.OK),
            (URL_RULES, HTTPStatus.OK),
            (lf('url_tree_detail'), HTTPStatus.FOUND),
            (lf('url_person_detail'), HTTPStatus.FOUND),
            (lf('url_user_profile'), HTTPStatus.FOUND),
    )
)
def test_pages_for_anonymous_user(url, expected_status, client):
    """Проверка, наличия и отсутствия доступа к страницам у анонимного пользователя."""
    response = client.get(url)
    assert response.status_code == expected_status



