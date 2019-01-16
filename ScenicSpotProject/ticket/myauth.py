from django.contrib.auth.models import User
from django.core.cache import caches
from rest_framework.authentication import BaseAuthentication

from administrator.models import Staff

admin_cache = caches['admin']
user_cache = caches['user']


class StaffAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.session.get('token')
        if not token:
            return None

        user_id = admin_cache.get(token)
        if not user_id:
            return None

        user = User.objects.filter(pk=user_id).first()
        staff = Staff.objects.filter(user=user).first()
        if staff:
            return staff, token

        return None
