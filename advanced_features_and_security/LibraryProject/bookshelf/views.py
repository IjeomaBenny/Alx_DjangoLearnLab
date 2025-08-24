from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login, logout
from .models import Book

# -----------------------------
# Login view
# -----------------------------
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')  # Redirect to book list after login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# -----------------------------
# Logout view
# -----------------------------
def user_logout(request):
    logout(request)
    return redirect('login')

# -----------------------------
# Book views with permissions
# -----------------------------
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        year = request.POST.get('publication_year')
        Book.objects.create(title=title, author=author, publication_year=year)
        return redirect('book_list')
    return render(request, 'bookshelf/book_create.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_edit.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})




# Create your views here.
