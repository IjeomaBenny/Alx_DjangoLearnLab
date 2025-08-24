from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='bookshelf/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),  # Add this line
]
