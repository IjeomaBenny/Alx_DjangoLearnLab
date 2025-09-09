from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Author
from .serializers import AuthorSerializer

class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.prefetch_related("books").all()
        return Response(AuthorSerializer(authors, many=True).data)


# Create your views here.
