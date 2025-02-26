import pytest
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.usefixtures('bunch_of_news')
def test_num_of_news_on_main(client, homepage_url):
    response = client.get(homepage_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('bunch_of_news')
def test_order_of_news(client, homepage_url):
    response = client.get(homepage_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.usefixtures('bunch_of_comments')
def test_oder_of_comments(client, news_detail_url):
    response = client.get(news_detail_url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'user, is_there_form',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True)
    )
)
def test_comment_form_for_different_users(
    user, is_there_form, news_detail_url
):
    response = user.get(news_detail_url)
    assert ('form' in response.context) == is_there_form
    if is_there_form:
        assert isinstance(response.context['form'], CommentForm)
