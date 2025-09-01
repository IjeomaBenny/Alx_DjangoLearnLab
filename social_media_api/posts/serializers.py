from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

# posts/serializers.py
from rest_framework import serializers
from .models import Post

class AuthorMiniSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)  # <- use related_name='likes'

    class Meta:
        model = Post
        fields = [
            "id", "author", "title", "content",
            "created_at", "updated_at",
            "comments_count", "likes_count"   # <- INCLUDE both here
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at", "comments_count", "likes_count"]

    def get_author(self, obj):
        return {"id": obj.author_id, "username": obj.author.username}


    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    def create(self, validated_data):
        # set author from request.user
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorMiniSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")
        return value

    def create(self, validated_data):
        # set author from request.user
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)
