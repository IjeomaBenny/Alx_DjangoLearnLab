import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Example data creation (with get_or_create to avoid duplicates)
def create_sample_data():
    author1, _ = Author.objects.get_or_create(name="Author One")
    author2, _ = Author.objects.get_or_create(name="Author Two")

    book1, _ = Book.objects.get_or_create(title="Book One", author=author1)
    book2, _ = Book.objects.get_or_create(title="Book Two", author=author1)
    book3, _ = Book.objects.get_or_create(title="Book Three", author=author2)

    library1, _ = Library.objects.get_or_create(name="Central Library")
    library2, _ = Library.objects.get_or_create(name="Community Library")

    # Add books to libraries (avoid duplicates)
    library1.books.add(book1, book3)
    library2.books.add(book2)

    Librarian.objects.get_or_create(name="Librarian A", library=library1)
    Librarian.objects.get_or_create(name="Librarian B", library=library2)


# Queries
def queries():
    # 1. Find all books by a specific author
    author_name = "Author One"
    books_by_author = Book.objects.filter(author__name=author_name)
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

    # 2. Find all books in a specific library
    library_name = "Central Library"
    library = Library.objects.get(name=library_name)
    print(f"Books in {library.name}: {[book.title for book in library.books.all()]}")


if __name__ == "__main__":
    create_sample_data()
    queries()
