from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("authors/", views.list_authors, name="list_authors"),
    path("libraries/", views.list_libraries, name="list_libraries"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
]
