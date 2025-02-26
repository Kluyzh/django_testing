from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .common import (ADD_URL, DELETE_URL, EDIT_URL, LOGIN_URL, SUCCESS_URL,
                     CommonData)


class TestLogic(CommonData):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note_data = {
            'title': 'New Title',
            'text': 'New text',
            'slug': 'new_slug'
        }

    def test_auth_user_can_create_a_note(self):
        notes_before = Note.objects.count()
        response = self.author_client.post(ADD_URL, data=self.note_data)
        notes_after = Note.objects.count()
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(notes_before + 1, notes_after)

    def test_anonymous_cant_create_a_note(self):
        notes_before = Note.objects.count()
        response = self.client.post(ADD_URL, data=self.note_data)
        redirect_url = f'{LOGIN_URL}?next={ADD_URL}'
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Note.objects.count(), notes_before)

    def test_notes_with_the_same_slug_cant_be_made(self):
        note = Note.objects.create(
            title='title of the note',
            text='note text',
            slug=self.note_data['slug'],
            author=self.reader
        )
        notes_before = Note.objects.count()
        response = self.author_client.post(ADD_URL, data=self.note_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), notes_before)

    def test_empty_slug(self):
        notes_before = Note.objects.count()
        self.note_data.pop('slug')
        response = self.author_client.post(ADD_URL, data=self.note_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), notes_before + 1)
        new_note = Note.objects.get(title=self.note_data['title'])
        expected_slug = slugify(self.note_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_a_note(self):
        response = self.author_client.post(EDIT_URL, self.note_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.note.refresh_from_db()
        self.assert_equality_of_note_and_data(self.note_data)

    def test_author_can_delete_a_note(self):
        response = self.author_client.post(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 0)

    def assert_equality_of_note_and_data(self, data):
        self.assertEqual(self.note.title, data['title'])
        self.assertEqual(self.note.text, data['text'])
        self.assertEqual(self.note.slug, data['slug'])

    def test_other_user_cant_edit_note(self):
        response = self.reader_client.post(EDIT_URL, self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(pk=self.note.id)
        self.assert_equality_of_note_and_data({
            'title': note_from_db.title,
            'text': note_from_db.text,
            'slug': note_from_db.slug,
        })

    def test_other_user_cant_delete_note(self):
        notes_before = Note.objects.count()
        response = self.reader_client.post(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_before)
