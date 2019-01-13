import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import caches
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .mythrottles import MyThrottles
from .until import generate_code
from .auth import SuperAdminAuth
from .models import SuperAdmin
from .serializer import UserSerializer, SuperAdminSerializer
from .tasks import send_code

user_cache = caches['user']


# 只可注册一次。
class SuperAdminRegister(ListCreateAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        return Response({'code': 1, 'msg': '假装注册页面'})

    def create(self, request, *args, **kwargs):
        if SuperAdmin.objects.all().exists():
            return Response({'code': 0, 'msg': '无法注册'})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(username=serializer.data.get('username'))
        user.set_password(user.password)
        user.is_superuser = True
        user.save()

        superuser = SuperAdmin.objects.create(user=user, phone=request.data.get('phone'))
        superuserserializer = SuperAdminSerializer(superuser)

        return Response(superuserserializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 使用该接口时直接向 管理员邮箱发送验证码。登录必须验证验证码
# 为防止 其他人  误访问  其实应该有限制只对 而且  应该是点击按钮才会发送。。。
# 应该是手机发送  而不是邮箱验证码
# 可以加个 节流设置 一天只准 访问 5次 之类  如果是真正管理员  不至于 访问五次登不进去
class SuperAdminLogin(ListCreateAPIView):
    serializer_class = SuperAdminSerializer

    # throttle_classes = (MyThrottles, )

    def get(self, request, *args, **kwargs):
        code = generate_code()
        send_code.delay('2942035955@qq.com', code)
        # 保存到缓存一份
        user_cache.set('check_code', code, 60*5)     # 五分钟失效
        return Response(data={'code': 1, 'msg': '假装登录页面'})

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

        # 自定义验证 可以使用 用户名密码 邮箱登录
        superadmin = authenticate(request=request, username=username, password=password)
        print(superadmin)
        if superadmin:

            token = uuid.uuid4().hex    # 生成随机token  当做 key值
            # redis缓存中 token 当做 key 值  保存 用户 id
            user_cache.set(token, superadmin.id, settings.SUPER_ADMIN_ALIVE)
            request.session['token'] = token    # 保存到 浏览器中一份

            return redirect(reverse('administrator:scenicspot'))

        return redirect(reverse('administrator:superadminlogin'))


# 原设想二次验证成功 则跳转到  超级管理员的  主页
# 可以添加  删除 游乐场  管理员信息
'''
class SecondCheckLogin(ListCreateAPIView):
    serializer_class = SuperAdminSerializer
    authentication_classes = (SuperAdminAuth, )

    def get(self, request, *args, **kwargs):
        superadmin = request.user

        # 如果是AnonymousUser表示返回值为空验证未通过
        if isinstance(superadmin, AnonymousUser):
            return Response({'code': 1, 'msg': '警告'})

        # 发送邮件。

        return Response(data={'code': 1, 'msg': '二次验证页面'})

    def post(self, request, *args, **kwargs):

        # 获取管理员输入的 验证码 判断是否与 缓存中保存的一致
        check_code = request.data.get('check_code')


        response = redirect(reverse('administrator:scenicspot'))
        response.delete_cookie('token')

        return response
'''


class ScenicSpotAPIView(APIView):

    authentication_classes = (SuperAdminAuth, )

    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'code': 1, 'msg': '没有权限'})

        return HttpResponse('hhh')
