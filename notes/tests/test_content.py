from django.test import TestCase, Client
from notes.models import Note
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Создатель заметки')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author)
        cls.user = Client()
        cls.user.force_login(cls.author)

    def test_notes(self):
        self.url = reverse('notes:list')
        response = self.user.get(self.url)
        object_list = response.context['object_list']
        self.assertIn(self.notes, object_list)

    def test_form_add(self):
        url = reverse('notes:add')
        response = self.user.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_form_edit(self):
        url = reverse('notes:edit', args=(self.notes.slug,))
        response = self.user.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
