from django.urls import path
from .views import list_books, list_authors, list_libraries, LibraryDetailView

from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("authors/", list_authors, name="list_authors"),
    path("libraries/", list_libraries, name="list_libraries"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
]




urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]

