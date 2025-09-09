from datetime import date
from rest_framework import serializers
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of Book.
    Includes validation: publication_year cannot be in the future.
    """
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (>{current_year})."
            )
        # (Optional) sanity bound for very old years
        if value < 0:
            raise serializers.ValidationError("publication_year must be positive.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes an Author with nested books.
    - name: the author's name
    - books: nested list of the author's related books (read-only by default)
    Relationship handling:
      related_name='books' on Book.author lets us access Author.books to nest.
    """

    """
Serializers for Author and Book.

- BookSerializer: serializes all fields of Book and validates that
  publication_year is not in the future.

- AuthorSerializer: serializes Author plus a nested, read-only list of
  the author's Books via related_name="books".
"""

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
