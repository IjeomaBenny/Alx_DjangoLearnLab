from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    home_view,
    list_books, add_book, edit_book, delete_book,
    list_authors, list_libraries, LibraryDetailView,
    admin_view, librarian_view, member_view,
    register_view,
)

urlpatterns = [
    # Homepage
    path("", home_view, name="home"),

    # Book views
    path("books/", list_books, name="list_books"),
    path("add_book/", add_book, name="add_book"),
    path("edit_book/<int:book_id>/", edit_book, name="edit_book"),
    path("delete_book/<int:book_id>/", delete_book, name="delete_book"),

    # Author & Library views
    path("authors/", list_authors, name="list_authors"),
    path("libraries/", list_libraries, name="list_libraries"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # Role-based views
    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),

    # Authentication
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
]
