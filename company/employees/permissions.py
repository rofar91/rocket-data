from rest_framework.permissions import BasePermission


class APICustomersGroupPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(user and (user.groups.filter(name='api_customers') or user.is_staff))
