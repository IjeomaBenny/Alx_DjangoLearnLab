from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer


from .models import Book
from .serializers import BookSerializer



from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.prefetch_related("books").all()
        return Response(AuthorSerializer(authors, many=True).data)
    



# GET /books/ — list all books (public, paginated, filterable)
class BookListView(generics.ListAPIView):
    """
    Lists books with filtering, searching, and ordering.
    - Filters: ?publication_year=1999&author=<author_id>
               ?min_year=1980&max_year=2000  (custom; see get_queryset)
    - Search:  ?search=potter  (matches title and author name)
    - Order:   ?ordering=publication_year or ?ordering=-publication_year
    """

    """
    ListAPIView for all books.
    - Permissions: Public read-only
    - Supports filters: publication_year, author
    - Supports custom range (min_year, max_year)
    - Supports search on title/author name
    - Supports ordering by publication_year, title, id
    """
    queryset = Book.objects.select_related("author").all().order_by("-id")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["publication_year", "author"]      # exact filters
    search_fields = ["title", "author__name"]              # icontains search
    ordering_fields = ["publication_year", "title", "id"]  # allowed ordering fields

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
    Retrieves a single Book by ID.
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# POST /books/create/ — create (authenticated)
class BookCreateView(generics.CreateAPIView):
    """
    Creates a new Book.
    Validation:
      - Serializer enforces publication_year not in future.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Hook for side effects (e.g., audit logs). We just save.
        serializer.save()


# PUT/PATCH /books/<pk>/update/ — update (authenticated)
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing Book.
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
    Deletes a Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



    



# Create your views here.
