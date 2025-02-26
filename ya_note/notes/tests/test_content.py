from notes.forms import NoteForm

from .common import ADD_URL, EDIT_URL, LIST_URL, CommonData


class TestContent(CommonData):

    def test_note_in_object_list(self):
        response = self.author_client.get(LIST_URL)
        self.assertIn(self.note, response.context['object_list'])

    def test_note_not_in_object_list(self):
        response = self.reader_client.get(LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_form_in_page(self):
        for url in (EDIT_URL, ADD_URL):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
