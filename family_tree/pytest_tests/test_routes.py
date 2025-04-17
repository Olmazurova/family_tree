from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf

from family_tree.pytest_tests.conftest import author_tree_client

from .conftest import (
    URL_HOME, URL_REG, URL_LOGIN, URL_RULES, URL_TREE_CREATE,
    URL_TREE_LIST, URL_USER_LOGOUT, URL_USER_EDIT
)


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

@pytest.mark.parametrize(
    'url, expected_status',
    (
            (URL_TREE_CREATE, HTTPStatus.OK),
            (URL_TREE_LIST, HTTPStatus.OK),
            (URL_USER_EDIT, HTTPStatus.OK),
            (URL_USER_LOGOUT, HTTPStatus.OK),
            (lf('url_user_profile'), HTTPStatus.OK),
            (lf('url_tree_detail'), HTTPStatus.OK),
            (lf('url_tree_structure'), HTTPStatus.OK),
            (lf('url_person_detail'), HTTPStatus.OK),
            (lf('url_tree_edit'), HTTPStatus.FOUND),
            (lf('url_tree_delete'), HTTPStatus.FOUND),
            (lf('url_person_edit'), HTTPStatus.FOUND),
            (lf('url_person_delete'), HTTPStatus.FOUND),
            (lf('url_person_create'), HTTPStatus.FOUND),
            (lf('url_non_public_tree_detail'), HTTPStatus.NOT_FOUND),
            (lf('url_non_public_person_detail'), HTTPStatus.NOT_FOUND),
            (lf('url_non_public_tree_structure'), HTTPStatus.NOT_FOUND),
    )
)
def test_pages_for_auth_user(another_user_client, url, expected_status):
    """Проверка наличия и отсутствия доступа к страницам у зарегистрированного пользователя."""
    response = another_user_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_status',
    (
            (lf('url_tree_edit'), HTTPStatus.OK),
            (lf('url_tree_delete'), HTTPStatus.OK),
            (lf('url_person_edit'), HTTPStatus.OK),
            (lf('url_person_delete'), HTTPStatus.OK),
            (lf('url_person_create'), HTTPStatus.OK),
            (lf('url_non_public_tree_detail'), HTTPStatus.OK),
            (lf('url_non_public_person_detail'), HTTPStatus.OK),
            (lf('url_non_public_tree_structure'), HTTPStatus.OK),
    )
)
def test_availability_pages_for_author(author_tree_client, url, expected_status):
    """Проверка наличия доступа к страницам у автора."""
    response = author_tree_client.get(url)
    assert response.status_code == expected_status
