from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_moderator)


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if getattr(request.user, "is_moderator", False):
            return True
        owner = getattr(obj, "owner", None) or getattr(obj, "created_by", None)
        return owner == request.user

