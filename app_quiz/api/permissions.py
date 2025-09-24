from rest_framework import permissions

class IsOwnerStaffOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an quiz object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        is_owner = obj.owner == request.user
        is_admin = request.user.is_staff or request.user.is_superuser
        return is_owner or is_admin