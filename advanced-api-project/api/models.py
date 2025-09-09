from django.db import models

class Author(models.Model):
    """
    Author represents a writer/creator.
    One Author can have many Book records (one-to-many).
    Fields:
        - name: the author's display name.
    """
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Book(models.Model):


    
    """
    Book belongs to a single Author (ForeignKey).
    Fields:
        - title: title of the book.
        - publication_year: year the book was published (int).
        - author: FK to Author (one-to-many relation).
    """

    
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"  # lets us access author.books
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"


# Create your models here.
