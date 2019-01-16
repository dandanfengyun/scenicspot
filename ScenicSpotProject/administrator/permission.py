from django.contrib.auth.models import User, AnonymousUser
from rest_framework.permissions import BasePermission


class SuperAdminPermission(BasePermission):

    def has_permission(self, request, view):
        superadmin = request.user
        if not isinstance(superadmin, AnonymousUser):
            user = superadmin.user
            return user.is_superuser
        return False


class AdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        adminuser = request.user
        if not isinstance(adminuser, AnonymousUser):
            if adminuser.is_adminuser:
                return True
        return False
