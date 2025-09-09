from django.urls import path
from .views import AuthorListAPIView


# api/urls.py
from django.urls import path
from . import views  # import the views module

urlpatterns = [
    path("authors/", views.AuthorListAPIView.as_view(), name="author-list"),

    path("books/", views.BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("books/create/", views.BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/update/", views.BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book-delete"),
]

