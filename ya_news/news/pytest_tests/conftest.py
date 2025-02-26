from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News

from .constants import (AUTHOR_COMMENT, COMMENT_DELETE, COMMENT_EDIT, HOMEPAGE,
                        NEWS_DETAIL, USERS_LOGIN, USERS_LOGOUT, USERS_SIGNUP)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='not_author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news_object():
    return News.objects.create(
        title='Weather forecast',
        text='Today is a good day'
    )


@pytest.fixture
def comment_of_author(author, news_object):
    return Comment.objects.create(
        news=news_object,
        text=AUTHOR_COMMENT,
        author=author
    )


@pytest.fixture
def bunch_of_news():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'News number {index}',
            text=f'Text of news number {index}',
            date=today - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def bunch_of_comments(author, news_object):
    today = datetime.today()
    all_comments = [
        Comment(
            author=author,
            news=news_object,
            text=f'Comment number {index}',
            created=today - timedelta(days=index)
        ) for index in range(10)
    ]
    Comment.objects.bulk_create(all_comments)


@pytest.fixture
def homepage_url():
    return reverse(HOMEPAGE)


@pytest.fixture
def news_detail_url(news_object):
    return reverse(NEWS_DETAIL, args=(news_object.pk,))


@pytest.fixture
def comment_edit_url(comment_of_author):
    return reverse(COMMENT_EDIT, args=(comment_of_author.pk,))


@pytest.fixture
def comment_delete_url(comment_of_author):
    return reverse(COMMENT_DELETE, args=(comment_of_author.pk,))


@pytest.fixture
def login_url():
    return reverse(USERS_LOGIN)

@pytest.fixture
def logout_url():
    return reverse(USERS_LOGOUT)

@pytest.fixture
def signup_url():
    return reverse(USERS_SIGNUP)


