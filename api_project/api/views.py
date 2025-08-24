from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access



# BookViewSet uses ModelViewSet to provide CRUD operations.
# Only authenticated users with a valid token can access these endpoints.
# Token can be obtained by POSTing username & password to /api-token-auth/

   


# Create your views here.
