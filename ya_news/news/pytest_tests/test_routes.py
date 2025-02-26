from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

ANONYMOUS_CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
HOMEPAGE_URL = pytest.lazy_fixture('homepage_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
USERS_LOGIN_URL = pytest.lazy_fixture('login_url')
USERS_LOGOUT_URL = pytest.lazy_fixture('logout_url')
USERS_SIGNUP_URL = pytest.lazy_fixture('signup_url')


@pytest.mark.parametrize(
    'url, user, expected_status_code',
    (
        (HOMEPAGE_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (USERS_LOGIN_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (USERS_LOGOUT_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (USERS_SIGNUP_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_page_availability_for_different_users(
    user, url, expected_status_code
):
    response = user.get(url)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize('url', (COMMENT_EDIT_URL, COMMENT_DELETE_URL))
def test_redirection_of_anonymous(url, client, login_url):
    response = client.get(url)
    assertRedirects(response, f'{login_url}?next={url}')
