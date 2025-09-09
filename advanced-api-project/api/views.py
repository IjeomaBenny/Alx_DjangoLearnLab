# api/views.py
# api/views.py
from django.shortcuts import render  # optional; safe to keep
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter


class AuthorListAPIView(APIView):
    """
    GET /authors/ — Return all authors with nested books.
    """
    def get(self, request):
        authors = Author.objects.prefetch_related("books").all()
        return Response(AuthorSerializer(authors, many=True).data)


# GET /books/ — list all books (public, paginated, filterable)
class BookListView(generics.ListAPIView):
    """
    Lists books with filtering, searching, and ordering.
    - Filters (via filterset): ?title=fall  ?author=1  ?publication_year=1960
      Range: ?min_year=1950&max_year=1970
    - Search: ?search=achebe  (matches title and author name)
    - Order:  ?ordering=publication_year or ?ordering=-publication_year
    """
    queryset = Book.objects.select_related("author").all().order_by("-id")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter                      # <— use our FilterSet
    search_fields = ["title", "author__name"]
    ordering_fields = ["publication_year", "title", "id"]
    
    def get_queryset(self):
        qs = super().get_queryset()
        # Optional range filters:
        min_year = self.request.query_params.get("min_year")
        max_year = self.request.query_params.get("max_year")
        if min_year:
            qs = qs.filter(publication_year__gte=min_year)
        if max_year:
            qs = qs.filter(publication_year__lte=max_year)
        return qs


# GET /books/<pk>/ — retrieve one (public)
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single Book by ID.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# POST /books/create/ — create (authenticated)
class BookCreateView(generics.CreateAPIView):
    """
    Create a new Book.
    Validation:
      - Serializer enforces publication_year not in the future.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Hook for side effects (e.g., audit logs).
        serializer.save()


# PUT/PATCH /books/<pk>/update/ — update (authenticated)
class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing Book.
    PUT = full update, PATCH = partial update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Hook for custom business rules if needed.
        serializer.save()


# DELETE /books/<pk>/delete/ — delete (authenticated)
class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
