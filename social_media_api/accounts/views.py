from django.shortcuts import render

# accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user).key
        return Response({
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }, status=201)

class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        auth_response = super().post(request, *args, **kwargs)
        token = auth_response.data['token']
        user = Token.objects.get(key=token).user
        return Response({
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # enable image upload via multipart form
    parsers = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


# Create your views here.
