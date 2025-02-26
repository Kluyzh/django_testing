from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

from .constants import (ADD, DELETE, DETAIL, EDIT, HOME, LIST, LOGIN, LOGOUT,
                        SIGNUP, SUCCESS)

SLUG = 'slug_1'
LIST_URL = reverse(LIST)
EDIT_URL = reverse(EDIT, args=(SLUG,))
ADD_URL = reverse(ADD)
SUCCESS_URL = reverse(SUCCESS)
LOGIN_URL = reverse(LOGIN)
DELETE_URL = reverse(DELETE, args=(SLUG,))
HOMEPAGE_URL = reverse(HOME)
LOGOUT_URL = reverse(LOGOUT)
SIGNUP_URL = reverse(SIGNUP)
DETAIL_URL = reverse(DETAIL, args=(SLUG,))

User = get_user_model()


class CommonData(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.author = User.objects.create(username='author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='reader')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Title of the note',
            text='Note text',
            slug=SLUG,
            author=cls.author
        )
