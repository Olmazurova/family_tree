from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('home', 'registration', 'login', 'rules')
)
def test_pages_for_anonymous_user(name, client):
    """Проверка, что анонимный пользователь может заходить на страницы."""
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK



