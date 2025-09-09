import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    # case-insensitive partial match on title
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    # filter by author id (exact)
    author = django_filters.NumberFilter(field_name="author")
    # year filters
    publication_year = django_filters.NumberFilter(field_name="publication_year", lookup_expr="exact")
    min_year = django_filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    max_year = django_filters.NumberFilter(field_name="publication_year", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ["title", "author", "publication_year", "min_year", "max_year"]
