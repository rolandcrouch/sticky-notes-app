from django.db import models

# Create your models here.

class Note(models.Model):
    """
    Represents a sticky note with a title, content, and timestamp.
    Used for creating, displaying, editing, and deleting notes in 
    the application.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title