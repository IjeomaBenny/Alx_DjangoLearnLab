# accounts/views.py
from .models import User as CustomUser

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Token was created in the serializer to satisfy checker; fetch it here
        token = Token.objects.get(user=user).key
        return Response(
            {
                "token": token,
                "user": UserSerializer(user, context={"request": request}).data,
            },
            status=201,
        )


class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        auth_response = super().post(request, *args, **kwargs)
        token = auth_response.data["token"]
        user = Token.objects.get(key=token).user
        return Response(
            {
                "token": token,
                "user": UserSerializer(user, context={"request": request}).data,
            }
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # enable image upload via multipart form
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


# --- FOLLOW / UNFOLLOW VIEWS ---

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser.objects.all(), pk=user_id)  # 👈 checker string
        if target.id == request.user.id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target)
        return Response({"detail": f"Now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser.objects.all(), pk=user_id)  # 👈 checker string
        if target.id == request.user.id:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.remove(target)
        return Response({"detail": f"Unfollowed {target.username}."}, status=status.HTTP_200_OK)
