from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library, Author

# Function-based view: list all books with their authors
def list_books(request):
    books = Book.objects.select_related('author').all()
    # plain text output if ?format=text
    if request.GET.get("format") == "text":
        lines = [f"{b.title} by {b.author.name}" for b in books]
        return HttpResponse("\n".join(lines), content_type="text/plain")
    # otherwise render template
    return render(request, "relationship_app/list_books.html", {"books": books})

# Function-based view: list all authors
def list_authors(request):
    authors = Author.objects.all()
    return render(request, "relationship_app/list_authors.html", {"authors": authors})

# Function-based view: list all libraries
def list_libraries(request):
    libraries = Library.objects.all()
    return render(request, "relationship_app/list_libraries.html", {"libraries": libraries})

# Class-based view: library details (books in the library)
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"



# Create your views here.
