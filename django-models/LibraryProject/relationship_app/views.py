from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required   # <-- separate line


from .models import Library, Book, Author, UserProfile

# -----------------------------
# Home view
# -----------------------------
def home_view(request):
    return render(request, 'relationship_app/home.html')


# -----------------------------
# Function-based views
# -----------------------------
def list_books(request):
    books = Book.objects.all()
    if request.GET.get("format") == "text":
        lines = [f"{b.title} by {b.author.name}" for b in books]
        return HttpResponse("\n".join(lines), content_type="text/plain")
    return render(request, "relationship_app/list_books.html", {"books": books})


def list_authors(request):
    authors = Author.objects.all()
    return render(request, "relationship_app/list_authors.html", {"authors": authors})


def list_libraries(request):
    libraries = Library.objects.all()
    return render(request, "relationship_app/list_libraries.html", {"libraries": libraries})


# -----------------------------
# Authentication Views
# -----------------------------
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')


# -----------------------------
# Helper function for role-based access
# -----------------------------
def has_role(user, role_name):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role_name


# -----------------------------
# Role-based Views
# -----------------------------
@user_passes_test(lambda u: has_role(u, 'Admin'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(lambda u: has_role(u, 'Librarian'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(lambda u: has_role(u, 'Member'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# -----------------------------
# Class-based view: library details
# -----------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# -----------------------------
# Book Permission Views
# -----------------------------
# Add Book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = get_object_or_404(Author, id=author_id)
        Book.objects.create(title=title, author=author)
        return redirect('list_books')
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


# Edit Book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect('list_books')
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})


# Delete Book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

