from django.urls import path
from .views import list_books, list_authors, list_libraries, LibraryDetailView

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("authors/", list_authors, name="list_authors"),
    path("libraries/", list_libraries, name="list_libraries"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
]


