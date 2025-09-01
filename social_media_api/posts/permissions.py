from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Read for anyone (GET/HEAD/OPTIONS).
    Write/Update/Delete only if request.user is the object's author.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj has 'author' in both Post and Comment
        return getattr(obj, "author_id", None) == getattr(request.user, "id", None)
