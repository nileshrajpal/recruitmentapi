from rest_framework import permissions


class IsApplicationPosterOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.posted_by.username == request.user.username or request.user.is_admin:
            return True
