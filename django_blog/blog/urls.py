from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostByTagListView   #import your tag view

from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    PostByTagListView, SearchResultsView
)

from .views import SearchResultsView, PostByTagListView  # keep your other imports too


urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # Auth
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

     # Posts (CRUD)
      # Post CRUD (checker-required routes)
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # List route (needed for templates/success_url)
    path('posts/', views.PostListView.as_view(), name='post-list'),


    # Comment routes
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/',     views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/',     views.CommentDeleteView.as_view(), name='comment-delete'),

    # Tags & search
     # Tags (checker looks for this exact pattern)
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),
   

    # search
    path("search/", SearchResultsView.as_view(), name="search"),  # <-- add/ensure this exact name


]



    # (optional) your homepage route if you have one already:
    # path('', views.index, name='index'),

