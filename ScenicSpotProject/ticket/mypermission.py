from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class StaffPermission(BasePermission):

    def has_permission(self, request, view):
        staff = request.user
        if not isinstance(staff, AnonymousUser):
            user = staff.user
            print(staff)
            return user.is_staff
        return False
