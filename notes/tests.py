from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from .models import Note

class NoteModelTestCase(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="Sample Note",
            content="This is a sample note for testing."
        )

    def test_note_creation(self):
        """
        Test that a Note object is created with the correct title and content.
        """
        self.assertEqual(self.note.title, "Sample Note")
        self.assertEqual(self.note.content, "This is a sample note for testing.")
        self.assertIsNotNone(self.note.created_at)

    def test_note_str_representation(self):
        """
        Test that the string representation of the Note is its title.
        """
        self.assertEqual(str(self.note), "Sample Note")

    def test_created_at_auto_set(self):
        """
        Test that created_at is automatically set close to now.
        """
        self.assertLessEqual(self.note.created_at, now())



# Create your tests here.
class NoteViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.note = Note.objects.create(title="Test Note", content="This is a test.")

    def test_note_list_view(self):
        """
        Test that the note list view returns a 200 status and uses the correct template.
        """
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertIn(self.note, response.context['notes'])

    def test_add_note_view_get(self):
        """
        Test that the add note view loads correctly with a GET request.
        """
        response = self.client.get(reverse('add_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/add_note.html')

    def test_add_note_view_post(self):
        """
        Test that a valid POST request creates a new note.
        """
        response = self.client.post(reverse('add_note'), {
            'title': 'New Note',
            'content': 'New note content'
        })
        self.assertEqual(response.status_code, 302)  # should redirect
        self.assertEqual(Note.objects.count(), 2)  # original + new

    def test_edit_note_view_get(self):
        """
        Test that the edit note view loads with the correct note data.
        """
        response = self.client.get(reverse('edit_note', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/edit_note.html')
        self.assertContains(response, self.note.title)

    def test_edit_note_view_post(self):
        """
        Test that submitting an edited note updates the note content.
        """
        response = self.client.post(reverse('edit_note', args=[self.note.id]), {
            'title': 'Updated Title',
            'content': 'Updated content'
        })
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')

    def test_delete_note_view(self):
        """
        Test that a note is deleted and the user is redirected to the list.
        """
        response = self.client.post(reverse('delete_note', args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())