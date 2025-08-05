# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note 
from .forms import NoteForm
from django.http import HttpResponse


def note_list(request):
    """
    Display a list of all notes stored in the database.
    Renders the 'note_list.html' template with the list of notes.
    """
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})


def add_note(request):
    """
    Handle creation of a new note.
    If the request is POST, validate and save the form.
    If GET, display an empty form for the user to fill.
    Renders the 'add_note.html' template.
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})


def edit_note(request, note_id):
    """
    Handle editing of an existing note.
    Retrieves the note by ID and either updates it 
    (POST) or pre-fills the form (GET).
    Renders the 'edit_note.html' template.
    """
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})


def delete_note(request, note_id):
    """
    Handle deletion of a note identified by its ID.
    After deletion, redirects to the note list view.
    """
    Note.objects.filter(id=note_id).delete()
    return redirect('note_list')