from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

from .constants import AUTHOR_COMMENT

COMMENT_DATA_FORM = {'text': 'New comment'}


def test_anonymous_cant_comment(client, news_detail_url):
    comments_before = Comment.objects.count()
    client.post(news_detail_url, COMMENT_DATA_FORM)
    comments_after = Comment.objects.count()
    assert comments_before == comments_after


def test_auth_user_can_comment(author, author_client, news_detail_url):
    Comment.objects.all().delete()
    response = author_client.post(news_detail_url, COMMENT_DATA_FORM)
    assert Comment.objects.count() == 1
    assertRedirects(response, f'{news_detail_url}#comments')
    comment = Comment.objects.get()
    assert comment.author == author
    assert comment.text == COMMENT_DATA_FORM['text']


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, news_detail_url, bad_word):
    bad_words_data = {'text': f'Some text, {bad_word}, end'}
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_own_comments(
        author_client, comment_of_author, comment_edit_url, news_detail_url
):
    expected_redirect = news_detail_url + '#comments'
    response = author_client.post(comment_edit_url, COMMENT_DATA_FORM)
    assertRedirects(response, expected_redirect)
    comment_of_author.refresh_from_db()
    assert comment_of_author.text == COMMENT_DATA_FORM['text']


def test_author_can_delete_own_comment(
        author_client, news_detail_url, comment_delete_url
):
    response = author_client.post(comment_delete_url)
    assertRedirects(response, news_detail_url + '#comments')
    assert Comment.objects.count() == 0
    assert Comment.objects.exists() is False


def test_not_author_cant_edit_comments(
        not_author_client, comment_of_author, comment_edit_url
):
    response = not_author_client.post(comment_edit_url, COMMENT_DATA_FORM)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_of_author.refresh_from_db()
    assert comment_of_author.text == AUTHOR_COMMENT


def test_not_author_cant_delete_comments(
        not_author_client, comment_delete_url
):
    response = not_author_client.post(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
