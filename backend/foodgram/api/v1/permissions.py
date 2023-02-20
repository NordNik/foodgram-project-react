from rest_framework import permissions


class IsAutheticatedOrRegistration(permissions.BasePermission):
    """Without token only registration is allowed"""
    def has_permission(self, request, view):
        return (request.method == 'POST')