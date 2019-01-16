from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.cache import caches
from rest_framework.authentication import BaseAuthentication

from .models import SuperAdmin, AdminUser

admin_cache = caches['admin']


# 验证登录
class MyBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)      # 根据用户名
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)     # 邮箱
            except User.DoesNotExist:
                try:
                    superadmin = SuperAdmin.objects.get(phone=username)     # 手机号
                    user = superadmin.user
                except SuperAdmin.DoesNotExist:
                    return None

        # 如果找到user  开始验证密码  后一个是看 user 是不是 is_active
        if user.check_password(password) and self.user_can_authenticate(user=user):
            return user

        return None


# 超级管理员登录状态的验证
class SuperAdminAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.session.get('token')
        if not token:
            return None

        s_id = admin_cache.get(token)
        if not s_id:
            return None

        superadmin = SuperAdmin.objects.filter(pk=s_id).first()
        if superadmin:
            return superadmin, token

        return None


class AdminUserAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.session.get('token')
        if not token:
            return None

        user_id = admin_cache.get(token)
        if not user_id:
            return None

        user = User.objects.filter(pk=user_id).first()
        adminuser = AdminUser.objects.filter(user=user).first()
        if adminuser:
            return adminuser, token

        return None
