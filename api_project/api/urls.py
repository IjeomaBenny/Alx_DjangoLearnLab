from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList
from .views import BookViewSet
from rest_framework.authtoken.views import obtain_auth_token # Import the built-in view for token generation


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'), # existing list view
    path('', include(router.urls)),  # all CRUD operations via the router
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), # for users to obtain their token:
]





