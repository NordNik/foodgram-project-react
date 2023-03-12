from rest_framework import permissions


'''class IsAutheticatedOrRegistration(permissions.BasePermission):
    """Without token only registration is allowed"""
    def has_permission(self, request, view):
        return (request.method == 'POST')'''


class RecipePermission(permissions.BasePermission):
    """Custom permission class"""
    def has_permission(self, request, view):
        """Authorised or read only"""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Unsave methods and GET method for shopping lists"""
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenicated
                and (obj.author == request.user or request.method == 'POST'))
        )
