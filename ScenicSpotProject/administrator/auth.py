from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.cache import caches
from rest_framework.authentication import BaseAuthentication

from .models import SuperAdmin


cache = caches['user']


# 验证登录
class MyBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 首先验证缓存中是否有 check_code  不存在 则 有可能 是 无意访问到的或者验证码到期
        real_code = cache.get('check_code')
        if not real_code:
            return None

        # 如果验证码 与 不同  则可能验证码过期
        post_code = request.data.get('code')
        if post_code != real_code:
            print(post_code)
            return None

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
        print('为什么')
        # 如果找到user  开始验证密码  后一个是看 user 是不是 is_active
        if user.check_password(password) and self.user_can_authenticate(user=user):
            # 如果查询到 返回superadmin
            return user.superadmin


# 登录状态的验证
class SuperAdminAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.session.get('token')
        if not token:
            return None

        s_id = cache.get(token)
        if not s_id:
            return None

        superadmin = SuperAdmin.objects.get(pk=s_id)
        if superadmin:
            return superadmin, token

        return None

