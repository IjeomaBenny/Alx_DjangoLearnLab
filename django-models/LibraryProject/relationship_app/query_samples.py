import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()


from relationship_app.models import Author, Book, Library, Librarian

# Example data creation
def create_sample_data():
    author1 = Author.objects.create(name="Author One")
    author2 = Author.objects.create(name="Author Two")

    book1 = Book.objects.create(title="Book One", author=author1)
    book2 = Book.objects.create(title="Book Two", author=author1)
    book3 = Book.objects.create(title="Book Three", author=author2)

    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="Community Library")

    library1.books.add(book1, book3)
    library2.books.add(book2)

    Librarian.objects.create(name="Librarian A", library=library1)
    Librarian.objects.create(name="Librarian B", library=library2)

# Queries
def queries():
    author = Author.objects.get(name="Author One")
    print(f"Books by {author.name}: {[book.title for book in author.books.all()]}")

    library = Library.objects.get(name="Central Library")
    print(f"Books in {library.name}: {[book.title for book in library.books.all()]}")
    print(f"Librarian for {library.name}: {library.librarian.name}")

if __name__ == "__main__":
    create_sample_data()
    queries()
