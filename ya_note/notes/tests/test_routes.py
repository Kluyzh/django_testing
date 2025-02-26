from http import HTTPStatus

from .common import (ADD_URL, DELETE_URL, DETAIL_URL, EDIT_URL, HOMEPAGE_URL,
                     LIST_URL, LOGIN_URL, LOGOUT_URL, SIGNUP_URL, SUCCESS_URL,
                     CommonData)


class TestRoutes(CommonData):

    def test_availability(self):
        urls_users_statuses = (
            (HOMEPAGE_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
            (LIST_URL, self.reader_client, HTTPStatus.OK),
            (SUCCESS_URL, self.reader_client, HTTPStatus.OK),
            (ADD_URL, self.reader_client, HTTPStatus.OK),
            (EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (DETAIL_URL, self.reader_client, HTTPStatus.NOT_FOUND),
            (EDIT_URL, self.author_client, HTTPStatus.OK),
            (DELETE_URL, self.author_client, HTTPStatus.OK),
            (DETAIL_URL, self.author_client, HTTPStatus.OK),
        )
        for url, user, expected_status in urls_users_statuses:
            with self.subTest(
                url=url, user=user, expected_status=expected_status
            ):
                response = user.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_anonymous_redirect(self):
        urls = (
            LIST_URL,
            SUCCESS_URL,
            ADD_URL,
            DETAIL_URL,
            EDIT_URL,
            DELETE_URL
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                redirect_url = f'{LOGIN_URL}?next={url}'
                self.assertRedirects(response, redirect_url)
