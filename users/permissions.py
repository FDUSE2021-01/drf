from rest_framework import permissions


class IsMyself(permissions.BasePermission):
    """
    Custom permission to only allow users to read or edit themselves.
    """

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
